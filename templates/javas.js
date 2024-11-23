
const button = document.getElementById('theme-toggle');
button.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    document.body.classList.toggle('light-theme');
});

const fileInput = document.getElementById('fileInput');
const progressBar = document.getElementById('progressBar');
const progress = document.getElementById('progress');
const remainingTimeDisplay = document.getElementById('remainingTime');
const preview = document.getElementById('preview');

fileInput.addEventListener('change', event => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        progress.style.display = 'block';
        const total = file.size;
        let startTime = null;

        reader.onprogress = function(e) {
            if (e.lengthComputable) {
                const loaded = e.loaded;
                const percentage = (loaded / total) * 100;
                progressBar.style.width = percentage + '%';

                // Вычисление оставшегося времени
                if (startTime === null) {
                    startTime = new Date();
                }
                const currentTime = new Date();
                const elapsedTime = (currentTime - startTime) / 1000; // в секундах
                const remainingTime = (elapsedTime / (loaded / total)) - elapsedTime; // оставшееся время
                remainingTimeDisplay.textContent = `Оставшееся время: ${remainingTime >= 0 ? Math.ceil(remainingTime) + ' секунд' : 'завершено!'}`;
            }
        };

        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            progress.style.display = 'none'; // Скрыть индикатор после загрузки
            remainingTimeDisplay.textContent = 'Загрузка завершена!';
        };

        reader.readAsDataURL(file);
    }
});
