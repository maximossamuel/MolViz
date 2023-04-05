$.ajax({
    url: "add-elements-to-table.html",
    type: "GET",
    dataType: "json",
    success: function(result){
        console.log("Hey there !!");

        var element = ''

        $.each(result, function(key, value){
            element += '<tr id=' + value.number + '>';
            element += '<td id="table-number">' + value.number + '</td>';
            element += '<td id="table-code">' + value.code + '</td>';
            element += '<td id="table-name">' + value.name + '</td>';
            element += '<td id="table-color1">' + value.color1 + '</td>';
            element += '<td id="table-color2">' + value.color2 + '</td>';
            element += '<td id="table-color3">' + value.color3 + '</td>';
            element += '<td id="table-radius">' + value.radius + '</td>';
            element += '<td><button id="button">Delete</button>'
            element += '</tr>'
        }
        );

        $('#table').append(element)
    },
    fail: function(result){
        console.log("lol cringe");
    }
});

$(document).ready(
    function()
    {
        console.log("Ready when yall is")

        $("#table").on('click', '#button', function(){
            var deleted_id = $(this).closest('tr').attr('id')
            $(this).closest('tr').remove();
            console.log(deleted_id);

            $.post("/delete-element.html",
            {
                mol_id: deleted_id
            }
            );
        })
    }
)