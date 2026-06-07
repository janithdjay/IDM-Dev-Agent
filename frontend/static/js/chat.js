document.addEventListener(

    "DOMContentLoaded",

    function () {

        const button =
            document.getElementById(
                "send-button"
            );

        button.addEventListener(

            "click",

            function () {

                alert(
                    "Sprint 25.1 complete.\n\nChat backend integration comes in Sprint 25.2."
                );

            }

        );

    }

);