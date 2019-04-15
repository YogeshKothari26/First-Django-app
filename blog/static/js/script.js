	$('#formsubmit1') {
    .ajaxForm({
        url : 'create_indicator', // or whatever
        dataType : 'json',
        success : function (response) {
            alert("The server says: " + response);
        }
    })
;