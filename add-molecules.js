$(document).ready(
    function()
    {
        console.log("Hi !!");

        $("#button").click(

            function()
            {
                var reader = new FileReader();
                var file = $("#sdf_file").prop('files')[0];
                alert(file.name);
                reader.readAsText(file);
                console.log(reader.result);
                reader.onload = function(e){
                    var file_data = reader.result;
                    console.log(file_data);
                    $.post("/molecule-add-handler.html",
                    {
                        name: $("#mol-name").val(),
                        file: file_data
                    }
                    );
                };
            }
        );
    }
);