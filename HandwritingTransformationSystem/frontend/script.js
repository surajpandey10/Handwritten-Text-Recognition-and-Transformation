document.getElementById('process-button').addEventListener('click', async () => {
    const fileInput = document.getElementById('image-upload');
    const file = fileInput.files[0];
    const reader = new FileReader();
    
    reader.onloadend = async () => {
        const imageBase64 = reader.result.split(',')[1];
        
        const fontSize = document.getElementById('font-size').value;
        const textColor = document.getElementById('text-color').value;
        const pageColor = document.getElementById('page-color').value;
        const pageWidth = document.getElementById('page-width').value;
        const pageHeight = document.getElementById('page-height').value;
        const handwritingStyle = document.getElementById('handwriting-option').value;
        
        const response = await fetch('http://127.0.0.1:5000/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imageBase64,
                font_size: fontSize,
                text_color: textColor,
                page_color: pageColor,
                page_width: pageWidth,
                page_height: pageHeight,
                handwriting_style: handwritingStyle
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            const outputImage = document.getElementById('output-image');
            outputImage.src = 'data:image/png;base64,' + result.processed_image;
            outputImage.style.display = 'block';
        } else {
            console.error('Error processing image:', response.statusText);
        }
    };
    
    if (file) {
        reader.readAsDataURL(file);
    }
});
