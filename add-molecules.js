$(document).ready(
    function()
    {
        console.log("Hi !!");

        $("#button").click(

            function()
            {
                if ($("#mol-name").val() == null || $("#sdf_file").prop('files')[0] == null){
                    alert("Something's not right. Please try again.")
                }
                var reader = new FileReader();
                var file = $("#sdf_file").prop('files')[0];
                reader.readAsText(file);
                console.log(reader.result);
                reader.onload = function(e){
                    var file_data = reader.result;
                    console.log(file_data);
                    if ($("#mol-name").val() != null && file_data != null && $("#mol-name").val() != ""){    
                        $.post("/molecule-add-handler.html",
                        {
                            name: $("#mol-name").val(),
                            file: file_data
                        }
                        );
                        alert("Uploaded file.");
                    }
                    else{
                        alert("Cannot upload file. Please try again")
                    }
                };
            }
        );
    }
);