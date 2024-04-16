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
    qrCodeButton.style.display = "block";
    let qrCodeOutput = document.getElementById("qrcode");
    qrCodeOutput.style.display = "none";
}

function hideQRScanner() {
    let qrCodeButton = document.getElementById("qr-code-button");
    qrCodeButton.style.display = "block";
    let qrCodeOutput = document.getElementById("qrcode");
    qrCodeOutput.style.display = "none";
}

function qrCallBack(data, decodedResult = "") {
    let phoneNumber = document.getElementById("phone");
    phoneNumber.value = data;
    hideQRScanner();
}

function qrNativeCallBack(data) {
    let phoneNumber = document.getElementById("phone");
    phoneNumber.value = data;
    return true;
}

function getNativeScanner() {
    window.Telegram.WebApp.showScanQrPopup({text: "Сканируй QR!"}, qrNativeCallBack);
}

function getCustomScanner() {
    const html5QrCode = new Html5Qrcode("qrcode");

    html5QrCode.start(
        {facingMode: "environment"},
        {
            fps: 10,
            qrbox: {width: 250, height: 250}
        },
        (decodedText, decodedResult) => {
            let phoneNumber = document.getElementById("phone");
            phoneNumber.value = decodedText;
            hideQRScanner();
            html5QrCode.stop();
        },
        (errorMessage) => {
            // hideQRScanner();
            // html5QrCode.stop();
        })
        .catch((err) => {
            // hideQRScanner();
            // html5QrCode.stop();
        });

    let qrCodeOutput = document.getElementById("qrcode");
    qrCodeOutput.style.display = "block";
    let qrCodeButton = document.getElementById("qr-code-button");
    qrCodeButton.style.display = "none";

}

function goBack() {
    window.history.back();
}