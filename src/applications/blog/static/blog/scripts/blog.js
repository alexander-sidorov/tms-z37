const like = function (element, post_id) {
    let api_url = "/b/post/" + post_id + "/like/";

    fetch(api_url, {
        method: "POST",
    }).then(
        resp => {
            resp.json().then(
                resp_payload => {
                    if (resp_payload.ok) {
                        element.textContent = resp_payload.nr_likes;
                    } else {
                        console.log(JSON.stringify(resp_payload));
                    }
                }
            );
        }
    );
}
