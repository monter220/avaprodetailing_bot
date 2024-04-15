function generateQR(number) {
    let qrCodeOutput = document.getElementById("qrcode");
    qrCodeOutput.innerHTML = "";

    let qrcode = new QRCode(qrCodeOutput, {
        text: number,
        width: 256,
        height: 256,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });

    qrCodeOutput.style.display = "block";

    let qrCodeButton = document.getElementById("qr-code-button");
    qrCodeButton.style.display = "none";
}

function hideQRCode(){
    let qrCodeButton = document.getElementById("qr-code-button");
    qrCodeButton.style.display = "flex";
    let qrCodeOutput = document.getElementById("qrcode");
    qrCodeOutput.style.display = "none";
}