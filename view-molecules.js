$.ajax({
    //console.log("Hi js");
    url: "add-molecules-to-table.html",
    type: "GET",
    dataType: "json",
    success: function(result){
        console.log("Hey !!");
        var molecule = ''

        $.each(result, function(key, value){
            molecule += '<tr id=' + value.number + '>';
            molecule += '<td>' + value.number + '</td>';
            molecule += '<td>' + value.name + '</td>';
            molecule += '<td>' + value.atom_no + '</td>';
            molecule += '<td>' + value.bond_no + '</td>';
            molecule += '<td><button id="view-button">View</button>'
            molecule += '<td><button id="delete-button">Delete</button>'
            molecule += '</tr>';
        }
        );

        $('#table').append(molecule)
    },
});

$(document).ready(
    function()
    {
        $("#table").on('click', '#delete-button', function(){
            var deleted_id = $(this).closest('tr').attr('id')
            $(this).closest('tr').remove();
            console.log(deleted_id);

            $.post("/delete-molecule.html",
            {
                molecule_id: deleted_id
            }
            );
        });

        $("#table").on('click', '#view-button', function(){
            var mol_id = $(this).closest('tr').attr('id')

            // $.ajax(
            //     {
            //         type: "POST",
            //         url:"view-molecule.html",
            //         data: JSON.stringify({"molecule_id": mol_id}),
            //         dataType: "json",
            //         contentType: "application/json",
            //         success: function(result){console.log(result)}
            //     }
            // )

            $.post("/view-molecule.html",
            {
                molecule_id: mol_id
            },function(data, status){
                    console.log(data)
                    $("#svg-display").empty();
                    $("#svg-display").append(data);
            })
        }
        )
    }
)