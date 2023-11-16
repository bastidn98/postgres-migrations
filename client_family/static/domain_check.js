$(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        var client = $('#client').val();
        var family_head = $('#family_head').val();
        $.post('/internal/validate-domains', {client: client, family_head: family_head}, function(response) {
            if (!response.isValid) {
                var message = 'The following client domains (' + response.invalidDomains.join(', ') + ') are not in the family head (' + response.headDomains.join(', ') + '). Are you sure you want to save this?';
                if (confirm(message)) {
                    // If user confirms, submit the form
                    $('form').unbind('submit').submit();
                }
            } else {
                // If domains are valid, submit the form
                $('form').unbind('submit').submit();
            }
        });
    });
});