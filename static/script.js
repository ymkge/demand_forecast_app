document.getElementById('predict-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const ad_spend = parseFloat(document.getElementById('ad_spend').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const day_of_week = document.getElementById('day_of_week').value;
    const resultText = document.getElementById('result-text');

    resultText.textContent = '予測中...';
    resultText.classList.remove('error');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ad_spend: ad_spend,
                temperature: temperature,
                day_of_week: day_of_week,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '予測に失敗しました。');
        }

        const data = await response.json();
        resultText.textContent = `${Math.round(data.predicted_sales)} 個`;

    } catch (error) {
        resultText.textContent = `エラー: ${error.message}`;
        resultText.classList.add('error');
    }
});
