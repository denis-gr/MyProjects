function sync_request(method, url, data) {
    xhr = new XMLHttpRequest()
    xhr.open(method, url, false)
    xhr.setRequestHeader("Authorization", "Token " + token)
    xhr.setRequestHeader('Content-type', 'application/json;')
    xhr.send(JSON.stringify(data))
    return xhr.response ? JSON.parse(xhr.response) : xhr.response
}


function request(method, url, fun, data) {
    xhr = new XMLHttpRequest()
    xhr.open(method, url, true)
    xhr.onload = () => {
        fun(xhr.response ? JSON.parse(xhr.response) : xhr.response)
    }
    xhr.setRequestHeader("Authorization", "Token " + token)
    xhr.setRequestHeader('Content-type', 'application/json;')
    xhr.send(JSON.stringify(data))
}

var fileInput = document.querySelector(".form-file")
var input = fileInput.querySelector('.form-file-input');
var label = fileInput.querySelector('.form-file-text');
input.addEventListener('change', function (e) {
    if (this.files && this.files.length > 1)
        fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files
            .length);
    else
        fileName = e.target.value.split('\\').pop();
    if (fileName)
        label.innerHTML = fileName;
});
