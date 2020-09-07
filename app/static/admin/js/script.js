$(document).ready(function(){
    $('.btn').click(function(event){
        var btnClic = $(event.target).closest('button');
        var idDemande = $(btnClic).attr('idDemande');

        if(idDemande){
            $('#rejeter').attr('id', idDemande);
            $('#accepter').attr('id', idDemande);
            var tr = $(btnClic).closest('tr');
            var td = $(tr).children('td');
            $('#acte').attr('url', $(td)[6].innerText);
            $('#plan').attr('url', $(td)[5].innerText);
            $('#numeroDemande').val($(td)[0].innerText);
            $('#date').val($(td)[1].innerText);
            $('#typeDemande').val($(td)[2].innerText);
            $('#numeroTerrain').val($(td)[3].innerText);
            $('#demandeur').val($(td)[4].innerText);
            $('#dimensionTerrain').val($(td)[7].innerText);
            $('#localisation').val($(td)[8].innerText);
        }
    })
    
    $('#acte').click(function(){
        window.open($('#acte')[0].attributes['url'].value, '_blank', 'fullscreen=yes'); 
    })

    $('#rejeter').click(function(){
        $.ajax({
            url : 'http://127.0.0.1:5000/rejeter/'+$('#rejeter').context.activeElement.attributes[2].value,
            success : function (data) {
                if(data == 1){
                    alert('Cette demande a été rejeter avec succés !');
                    location.reload();
                }
            },
            error : function () {
                alert("Erreur !!!");
            }
        }
    );
    })

    $('#accepter').click(function(){
        $.ajax({
            url : 'http://127.0.0.1:5000/accepter/'+$('#accepter').context.activeElement.attributes[2].value,
            success : function (data) {
                if(data == 1){
                    alert('Cette demande a été accepter avec succés !');
                    location.reload();
                }
            },
            error : function () {
                alert("Erreur !!!");
            }
        });
    })
    
})