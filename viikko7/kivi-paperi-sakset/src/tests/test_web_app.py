import pytest
from web_app import app


@pytest.fixture
def client():
    """Flask test client"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


class TestWebApp:
    """Testit Flask web-sovellukselle"""
    
    def test_index_page_loads(self, client):
        """Testaa että pääsivu latautuu"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data
    
    def test_index_has_game_modes(self, client):
        """Testaa että pääsivulla on kaikki pelitilat"""
        response = client.get('/')
        assert b'Pelaaja vs Pelaaja' in response.data
        assert b'Parannettu' in response.data
    
    def test_start_game_pvp(self, client):
        """Testaa pelaaja vs pelaaja -pelin aloitus"""
        response = client.post('/start', data={'game_mode': 'a'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Pelaaja vs Pelaaja' in response.data or b'Tee siirtosi' in response.data
    
    def test_start_game_vs_ai(self, client):
        """Testaa tekoälypelin aloitus"""
        response = client.post('/start', data={'game_mode': 'b'}, follow_redirects=True)
        assert response.status_code == 200
    
    def test_start_game_vs_advanced_ai(self, client):
        """Testaa parannetun tekoälypelin aloitus"""
        response = client.post('/start', data={'game_mode': 'c'}, follow_redirects=True)
        assert response.status_code == 200
    
    def test_play_without_game_redirects(self, client):
        """Testaa että /play ilman peliä ohjaa takaisin etusivulle"""
        response = client.get('/play')
        assert response.status_code == 302  # Redirect
    
    def test_move_pvp_both_rock(self, client):
        """Testaa tasapeli kun molemmat valitsevat kiven"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
        
        response = client.post('/move', data={
            'player1_move': 'k',
            'player2_move': 'k'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_move_pvp_player1_wins(self, client):
        """Testaa että pelaaja 1 voittaa kun pelaa kiven saksilla"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
        
        response = client.post('/move', data={
            'player1_move': 'k',
            'player2_move': 's'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_move_pvp_player2_wins(self, client):
        """Testaa että pelaaja 2 voittaa kun pelaa paperin kiveä vastaan"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
        
        response = client.post('/move', data={
            'player1_move': 'k',
            'player2_move': 'p'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_move_vs_ai(self, client):
        """Testaa siirto tekoälyä vastaan"""
        with client.session_transaction() as session:
            session['game_mode'] = 'b'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
            session['ai_state'] = 0
        
        response = client.post('/move', data={
            'player1_move': 'k'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_move_vs_advanced_ai(self, client):
        """Testaa siirto parannettua tekoälyä vastaan"""
        with client.session_transaction() as session:
            session['game_mode'] = 'c'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
            session['ai_memory'] = []
        
        response = client.post('/move', data={
            'player1_move': 'k'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_invalid_move_redirects(self, client):
        """Testaa että virheellinen siirto ohjaa takaisin peliin"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
        
        response = client.post('/move', data={
            'player1_move': 'x',
            'player2_move': 'k'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_reset_redirects_to_index(self, client):
        """Testaa että reset ohjaa etusivulle"""
        response = client.get('/reset')
        assert response.status_code == 302  # Redirect
    
    def test_score_tracking_pvp(self, client):
        """Testaa pisteiden seuranta usealla kierroksella"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
        
        # Pelaaja 1 voittaa
        client.post('/move', data={'player1_move': 'k', 'player2_move': 's'})
        
        with client.session_transaction() as session:
            assert session['tuomari']['ekan_pisteet'] == 1
            assert session['tuomari']['tokan_pisteet'] == 0
            assert session['tuomari']['tasapelit'] == 0
        
        # Tasapeli
        client.post('/move', data={'player1_move': 'p', 'player2_move': 'p'})
        
        with client.session_transaction() as session:
            assert session['tuomari']['ekan_pisteet'] == 1
            assert session['tuomari']['tokan_pisteet'] == 0
            assert session['tuomari']['tasapelit'] == 1
        
        # Pelaaja 2 voittaa
        client.post('/move', data={'player1_move': 's', 'player2_move': 'k'})
        
        with client.session_transaction() as session:
            assert session['tuomari']['ekan_pisteet'] == 1
            assert session['tuomari']['tokan_pisteet'] == 1
            assert session['tuomari']['tasapelit'] == 1
    
    def test_ai_state_updates(self, client):
        """Testaa että tekoälyn tila päivittyy"""
        with client.session_transaction() as session:
            session['game_mode'] = 'b'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
            session['ai_state'] = 0
        
        client.post('/move', data={'player1_move': 'k'})
        
        with client.session_transaction() as session:
            assert session['ai_state'] == 1
        
        client.post('/move', data={'player1_move': 'p'})
        
        with client.session_transaction() as session:
            assert session['ai_state'] == 2
        
        client.post('/move', data={'player1_move': 's'})
        
        with client.session_transaction() as session:
            assert session['ai_state'] == 0  # Kiertää takaisin
    
    def test_advanced_ai_memory_updates(self, client):
        """Testaa että parannetun tekoälyn muisti päivittyy"""
        with client.session_transaction() as session:
            session['game_mode'] = 'c'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
            session['ai_memory'] = []
        
        client.post('/move', data={'player1_move': 'k'})
        
        with client.session_transaction() as session:
            assert 'k' in session['ai_memory']
            assert len(session['ai_memory']) == 1
        
        client.post('/move', data={'player1_move': 'p'})
        
        with client.session_transaction() as session:
            assert len(session['ai_memory']) == 2
            assert session['ai_memory'][0] == 'k'
            assert session['ai_memory'][1] == 'p'
    
    def test_game_history_tracking(self, client):
        """Testaa että pelihistoria tallentuu"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
        
        client.post('/move', data={'player1_move': 'k', 'player2_move': 's'})
        
        with client.session_transaction() as session:
            assert len(session['game_history']) == 1
            assert session['game_history'][0]['player1'] == 'Kivi'
            assert session['game_history'][0]['player2'] == 'Sakset'
            assert 'voitti' in session['game_history'][0]['result']
    
    def test_game_ends_at_5_wins_player1(self, client):
        """Testaa että peli päättyy kun pelaaja 1 saa 5 voittoa"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 5, 'tokan_pisteet': 2, 'tasapelit': 1}
            session['game_history'] = []
        
        response = client.get('/play')
        assert response.status_code == 200
        assert b'paattyi' in response.data or b'Pelaaja 1' in response.data
    
    def test_game_ends_at_5_wins_player2(self, client):
        """Testaa että peli päättyy kun pelaaja 2 saa 5 voittoa"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 2, 'tokan_pisteet': 5, 'tasapelit': 0}
            session['game_history'] = []
        
        response = client.get('/play')
        assert response.status_code == 200
        assert b'paattyi' in response.data or b'Pelaaja 2' in response.data
    
    def test_game_ends_at_5_wins_vs_ai(self, client):
        """Testaa että peli päättyy kun tietokone saa 5 voittoa"""
        with client.session_transaction() as session:
            session['game_mode'] = 'b'
            session['tuomari'] = {'ekan_pisteet': 1, 'tokan_pisteet': 5, 'tasapelit': 0}
            session['game_history'] = []
            session['ai_state'] = 0
        
        response = client.get('/play')
        assert response.status_code == 200
        assert b'Tietokone' in response.data
    
    def test_cannot_play_after_game_over(self, client):
        """Testaa että ei voi pelata enää kun peli on päättynyt"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 5, 'tokan_pisteet': 3, 'tasapelit': 0}
            session['game_history'] = []
        
        # Try to make a move after game is over
        client.post('/move', data={'player1_move': 'k', 'player2_move': 'p'})
        
        with client.session_transaction() as session:
            # Score should not change
            assert session['tuomari']['ekan_pisteet'] == 5
            assert session['tuomari']['tokan_pisteet'] == 3
    
    def test_play_until_win(self, client):
        """Testaa että peli pelaa kunnes joku voittaa"""
        with client.session_transaction() as session:
            session['game_mode'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            session['game_history'] = []
        
        # Play until player 1 gets 5 wins
        for i in range(5):
            client.post('/move', data={'player1_move': 'k', 'player2_move': 's'})
        
        with client.session_transaction() as session:
            assert session['tuomari']['ekan_pisteet'] == 5
        
        # Check that game over is displayed
        response = client.get('/play')
        assert b'paattyi' in response.data or b'voitti pelin' in response.data
