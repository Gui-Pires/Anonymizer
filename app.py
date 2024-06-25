from flask import Flask, render_template, request, send_from_directory, jsonify
import shutil  # Adicionado para limpeza de diretório
import fitz  # PyMuPDF
import time
import re
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variável global para armazenar o progresso
progress = 0

# Padrões para identificar dados sensíveis
patterns = {
    'Email': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
    'Mailto': r'mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
    'CPF': r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b',
    'CNPJ': r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b',
    'RG': r'\b\d{2}\.\d{3}\.\d{3}-\d{1}\b',
    'CEP': r'\b\d{5}-\d{3}\b|\b\d{2}\.\d{3}-\d{3}\b',
    'Links': r'https?://[A-Za-z0-9./?=_-]+|www\.[A-Za-z0-9./?=_-]+',
    'Endereços': r'\b(Rua|Avenida|Av|Av.|Praça|Travessa|Alameda|Al|Rodovia|Estrada|R)\s+[A-Za-zÀ-ÿ0-9\s,.-]+'
}

'''
Função para verificar se um arquivo PDF está a mais de 1 hora na pasta uploads.
Caso esteja, o arquivo é excluído, assim como qualquer subdiretório.
'''
def clean_upload_folder():
	now = time.time()
	cutoff = now - 3600  # 1 hora atrás

	for filename in os.listdir(UPLOAD_FOLDER):
		file_path = os.path.join(UPLOAD_FOLDER, filename)
		if os.path.isfile(file_path) or os.path.islink(file_path):
			if os.path.getmtime(file_path) < cutoff:
				try:
					os.remove(file_path)
				except Exception as e:
					pass
		elif os.path.isdir(file_path):
			if os.path.getmtime(file_path) < cutoff:
				try:
					shutil.rmtree(file_path)
				except Exception as e:
					pass


# Função para identificar e anonimizar dados sensíveis no texto
def anonymize_text(page, patterns, headerBool):
	blocks = page.get_text("dict")["blocks"]
	headerSpan = 0
	for block in blocks:
		if block["type"] == 0:  # Texto
			for line in block["lines"]:
				for span in line["spans"]:
					text = span["text"]
					for pattern in patterns.values():
						for match in re.finditer(pattern, text):
							if (headerSpan <= 2 and headerBool == True):
								headerSpan += 1
							else:
								# Calcular a posição exata do texto sensível
								start = match.start()
								end = match.end()
								span_start_x = span["bbox"][0] + (span["bbox"][2] -	span["bbox"][0]) * (start / len(text))
								span_end_x = span["bbox"][0] + (span["bbox"][2] - span["bbox"][0]) * (end / len(text))
								rect = fitz.Rect(span_start_x - 1, span["bbox"][1], span_end_x + 1, span["bbox"][3])
								page.add_redact_annot(rect, fill=(0, 0, 0))
								headerSpan += 1
		elif block["type"] == 1:  # Imagem
			rect = fitz.Rect(block["bbox"])
			page.add_redact_annot(rect, fill=(1, 1, 1))
		elif block["type"] == 2:  # Desenho
			rect = fitz.Rect(block["bbox"])
			page.add_redact_annot(rect, fill=(0, 0, 0))
	page.apply_redactions()


'''
Função para anonimizar QR Codes em links.
Alguns documemtos possuem QR Codes em links que não são capturados como imagem.
'''
def anonymize_qr_codes_in_links(page):
	links = page.get_links()
	for link in links:
		uri = link.get("uri", "")
		if re.search(r'https?://', uri):  # Verificar se o link é uma URL
			rect = fitz.Rect(link["from"])
			page.add_redact_annot(rect, fill=(1, 1, 1))  # Usar branco para cobrir o QR Code


# Função para processar o PDF
def anonymize_pdf(input_pdf_path, output_pdf_path):
	global progress
	progress = 0
	doc = fitz.open(input_pdf_path)

	total_pages = len(doc)
	for page_num in range(total_pages):
		page = doc.load_page(page_num)

		# Anonimizar QR Codes em links
		anonymize_qr_codes_in_links(page)

		headerBool = True
		if (page_num >= total_pages - 2):
			headerBool = False

		# Anonimizar texto, imagens e desenhos
		anonymize_text(page, patterns, headerBool)

		page.apply_redactions()

		# Atualização de progresso
		progress = int((page_num + 1) / total_pages * 100)
		# time.sleep(0.1)  # Simulação de tempo de processamento

	doc.save(output_pdf_path)
	progress = 100


@app.route('/')
def index():
	global progress
	progress = 0  # Resetar o progresso ao carregar a página
	return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
	global progress
	progress = 0
	
	if 'file' not in request.files:
		return jsonify({'error': 'No file part'}), 400
	file = request.files['file']
	if file.filename == '':
		return jsonify({'error': 'No selected file'}), 400

	# Verificar se o arquivo é um PDF
	if not file.filename.lower().endswith('.pdf'):
		return jsonify({'error': 'File is not a PDF'}), 400

	try:
		pdf_file = fitz.open(stream=file.read(), filetype="pdf")
		file.seek(0)  # Reset the file pointer to the beginning after reading
	except Exception as e:
		return jsonify({'error': 'File is not a valid PDF'}), 400

	# Limpar a pasta de uploads antes de salvar o novo arquivo
	clean_upload_folder()

	if file:
		input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		output_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'],
		                               'anonymized_' + file.filename)
		file.save(input_pdf_path)
		anonymize_pdf(input_pdf_path, output_pdf_path)
		return jsonify({'file_path': output_pdf_path})


@app.route('/download/<filename>')
def download_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
	                           filename,
	                           as_attachment=True)


@app.route('/progress')
def get_progress():
	global progress
	return jsonify({'progress': progress})


if __name__ == '__main__':
	app.run('0.0.0.0', debug=True)
