
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "post_direction": 1})
    assert res.status_code == 201

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "post_direction": 0})
    assert res.status_code == 404

def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 4, "post_direction": 0})
    assert res.status_code == 404

def test_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 4, "post_direction": 1})
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "post_direction": 1})
    assert res.status_code == 401