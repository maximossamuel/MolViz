$(document).ready(
    function()
    {
        $("#button").click(

            function()
            {
                $.post("/molecule-add-handler.html",
                {
                    name: $("#mol-name").val(),
                    file: $("#sdf_file").val()
                }
                );
            }
        );
    }
);