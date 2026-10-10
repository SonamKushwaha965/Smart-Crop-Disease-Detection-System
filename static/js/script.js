// Smart Crop Disease Detection - Frontend JS
// Kaam: scroll reveal, file preview, drag-drop, form submit par loading overlay,
// result par confidence bar animation + auto-scroll

// ---------- Scroll reveal ----------
var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); } });
}, { threshold: .12 });
document.querySelectorAll('.reveal').forEach(function (el) { obs.observe(el); });

// ---------- Elements ----------
var dropZone   = document.getElementById('dropZone');
var fileInput  = document.getElementById('fileInput');
var previewWrap = document.getElementById('previewWrap');
var previewImg = document.getElementById('previewImg');
var submitBtn  = document.getElementById('submitBtn');
var uploadForm = document.getElementById('uploadForm');
var overlay    = document.getElementById('loadingOverlay');
var resultBox  = document.getElementById('resultBox');

var selectedFile = null;

// ---------- File select / drag-drop ----------
dropZone.addEventListener('click', function () { fileInput.click(); });
fileInput.addEventListener('change', function () { handleFile(fileInput.files[0]); });
dropZone.addEventListener('dragover', function (e) { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', function () { dropZone.classList.remove('dragover'); });
dropZone.addEventListener('drop', function (e) {
    e.preventDefault(); dropZone.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
    if (!file || !file.type.startsWith('image/')) {
        alert('Sirf image file (JPG/PNG) select karo!');
        return;
    }
    selectedFile = file;
    if (previewImg) {
        previewImg.src = URL.createObjectURL(file);
        previewWrap.style.display = 'block';
    }
    submitBtn.disabled = false;
}

// ---------- Form submit -> loading overlay ----------
uploadForm.addEventListener('submit', function () {
    if (!selectedFile && fileInput.files.length === 0) {
        alert('Pehle photo select karo!');
        return false;
    }
    overlay.style.display = 'flex';   // page reload se pehle dikhega
});

// ---------- Result dikhe to: bar animation + auto scroll ----------
window.addEventListener('load', function () {
    if (resultBox) {
        // confidence bar animate karo
        document.querySelectorAll('.conf-fill').forEach(function (el) {
            var w = el.getAttribute('data-w') + '%';
            requestAnimationFrame(function () { setTimeout(function () { el.style.width = w; }, 150); });
        });
        // result card tak smooth scroll
        setTimeout(function () { resultBox.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 400);
    }
});