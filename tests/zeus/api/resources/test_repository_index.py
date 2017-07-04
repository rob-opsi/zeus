import json

from zeus.testutils import assert_json_response


def test_repo_list(client, default_login, default_repo):
    resp = client.get('/api/repos')
    assert resp.status_code == 200
    assert_json_response(resp)
    data = json.loads(resp.data)
    assert len(data) == 1
    assert data[0]['id'] == str(default_repo.id)
