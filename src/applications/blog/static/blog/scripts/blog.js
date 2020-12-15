const like = function (element, post_absolute_url) {
    let api_url = `${post_absolute_url}like/`;

    fetch(api_url, {
        method: "POST",
    }).then(
        response => {
            if (response.status === 200) {
                response.json().then(
                    payload => {
                        if (payload.ok) {
                            element.textContent = payload.nr_likes;
                        } else {
                            console.log("ERROR (server declines request):", JSON.stringify(payload.reason));
                        }
                    }
                ).catch(
                    error => {
                        console.log("ERROR (while parsing server response):", error);
                    }
                );
            } else {
                console.log("ERROR (with response):", response.status, response.statusText);
            }
        }
    ).catch(
        error => {
            console.log("ERROR (on fetch request):", error);
        }
    );
}
