$(document).ready(function () {
	let checkProgress;

	$('#uploadForm').on('submit', function (e) {
		e.preventDefault();
		var formData = new FormData(this);

		// Resetar a barra de progresso
		$('.progress-bar').css('width', '0%').attr('aria-valuenow', 0).text('0%').removeClass('bg-success d-none');
		$('#progress').removeClass('d-none');
		$('#result').html(''); // Limpar a mensagem de resultado

		$.ajax({
			url: '/upload',
			type: 'POST',
			data: formData,
			processData: false,
			contentType: false,
			success: function (data) {
				if (data.error) {
					$('#result').html(`
						<div class="alert alert-danger" role="alert">
							${data.error}
						</div>
					`);
				} else {
					const filename = data.file_path.split('/').pop();
					$('#result').html(`
						<div class="alert alert-success py-1 px-2" role="alert">
							<p class="mb-1">PDF anonimizado com sucesso! <a href="/download/${filename}" class="alert-link">Download aqui.</a></p>
							<p class="text-end my-0"><small class="text-muted">*Verifique sempre se o arquivo está devidamente anonimizado.</small></p>
						</div>
					`);
					// clearInterval(checkProgress);
				}
			},
			error: function () {
				$('#result').html(`
					<div class="alert alert-danger" role="alert">
						Ocorreu um erro ao anonimizar o PDF. Tente novamente!
					</div>
				`);
				$('#progress').addClass('d-none');
				clearInterval(checkProgress);
			}
		});

		// Iniciar polling para verificar progresso
		checkProgress = setInterval(function () {
			$.getJSON('/progress', function (data) {
				const progress = data.progress;
				if (progress >= 100) {
					clearInterval(checkProgress);
					$('.progress-bar').addClass('bg-success');
				}
				$('.progress-bar').css('width', `${progress}%`).attr('aria-valuenow', progress).text(`${progress}%`);
			});
		}, 200);
	});
});