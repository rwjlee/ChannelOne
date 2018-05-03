function byteArrayToString(byteArray) {
    var str = "", i;
    for (i = 0; i < byteArray.length; ++i) {
        str += escape(String.fromCharCode(byteArray[i]));
    }
    return str;
}

function encryptPassword(password) {
    let shaEncrypted = CryptoJS.SHA256(password);
    return byteArrayToString(shaEncrypted.words);
}


function formToJson(formId) {
    let fields = $(formId).serializeArray();
    let json = {};

    for (let i in fields) {
        let inputField = fields[i];
        json[inputField['name']] = inputField['value'];
    }

    return json;
}


function displayErrors(target, errors) {
    for (let i = 0; i < errors.length; i++) {
        let flash = $("<div></div>").addClass("alert").addClass("alert-danger").addClass("message");
        flash.text(errors[i]);
        flash.appendTo(target);
    }
}


function createElement(tag, text, classes=[]) {
    let element = $("<"+tag+"><"+tag+"/>");
    for (let i = 0 ; i < classes.length ; i++) {
        element.addClass(classes[i]);
    }
    element.text(text);
    return element;
}




