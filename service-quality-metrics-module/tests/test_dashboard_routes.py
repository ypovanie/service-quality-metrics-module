from app import create_app



def test_dashboard_summary_route_returns_json():
    app = create_app()
    client = app.test_client()

    response = client.get('/dashboard/summary')

    assert response.status_code == 200
    payload = response.get_json()
    assert set(payload.keys()) == {
        'csat',
        'nps',
        'aht',
        'fcr',
        'sla_compliance',
        'requests_total',
    }
    assert payload['requests_total'] == 2
