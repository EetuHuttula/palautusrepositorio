from flask import Flask, render_template, request, session, redirect, url_for
from kps_tehdas import luo_peli
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    """Main page - game mode selection"""
    session.clear()
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_game():
    """Initialize the game with selected mode"""
    game_mode = request.form.get('game_mode')
    session['game_mode'] = game_mode
    session['tuomari'] = {
        'ekan_pisteet': 0,
        'tokan_pisteet': 0,
        'tasapelit': 0
    }
    session['game_history'] = []
    
    # Initialize AI if needed
    if game_mode == 'b':
        session['ai_state'] = 0
    elif game_mode == 'c':
        session['ai_memory'] = []
    
    return redirect(url_for('play'))


@app.route('/play')
def play():
    """Game play page"""
    game_mode = session.get('game_mode')
    if not game_mode:
        return redirect(url_for('index'))
    
    tuomari_data = session.get('tuomari', {})
    history = session.get('game_history', [])
    
    game_mode_names = {
        'a': 'Pelaaja vs Pelaaja',
        'b': 'Pelaaja vs Tekoäly',
        'c': 'Pelaaja vs Parannettu Tekoäly'
    }
    
    # Check if game is over (first to 5 wins)
    game_over = False
    winner = None
    if tuomari_data.get('ekan_pisteet', 0) >= 3:
        game_over = True
        winner = 'Pelaaja 1'
    elif tuomari_data.get('tokan_pisteet', 0) >= 3:
        game_over = True
        if game_mode == 'a':
            winner = 'Pelaaja 2'
        else:
            winner = 'Tietokone'
    
    return render_template('play.html', 
                         game_mode=game_mode,
                         game_mode_name=game_mode_names.get(game_mode, ''),
                         tuomari=tuomari_data,
                         history=history,
                         game_over=game_over,
                         winner=winner)


@app.route('/move', methods=['POST'])
def make_move():
    """Process a game move"""
    game_mode = session.get('game_mode')
    if not game_mode:
        return redirect(url_for('index'))
    
    # Check if game is already over
    tuomari_data = session.get('tuomari', {})
    if tuomari_data.get('ekan_pisteet', 0) >= 5 or tuomari_data.get('tokan_pisteet', 0) >= 5:
        return redirect(url_for('play'))
    
    player1_move = request.form.get('player1_move')
    
    # Validate player 1 move
    if player1_move not in ['k', 'p', 's']:
        return redirect(url_for('play'))
    
    # Get player 2 move based on game mode
    if game_mode == 'a':
        # Player vs Player
        player2_move = request.form.get('player2_move')
        if player2_move not in ['k', 'p', 's']:
            return redirect(url_for('play'))
    elif game_mode == 'b':
        # Basic AI
        ai_state = session.get('ai_state', 0)
        ai_state = (ai_state + 1) % 3
        session['ai_state'] = ai_state
        
        if ai_state == 0:
            player2_move = 'k'
        elif ai_state == 1:
            player2_move = 'p'
        else:
            player2_move = 's'
    else:  # game_mode == 'c'
        # Advanced AI
        ai_memory = session.get('ai_memory', [])
        
        if len(ai_memory) == 0 or len(ai_memory) == 1:
            player2_move = 'k'
        else:
            viimeisin_siirto = ai_memory[-1]
            k = 0
            p = 0
            s = 0
            
            for i in range(len(ai_memory) - 1):
                if viimeisin_siirto == ai_memory[i]:
                    seuraava = ai_memory[i + 1]
                    if seuraava == 'k':
                        k += 1
                    elif seuraava == 'p':
                        p += 1
                    else:
                        s += 1
            
            if k > p or k > s:
                player2_move = 'p'
            elif p > k or p > s:
                player2_move = 's'
            else:
                player2_move = 'k'
        
        # Update AI memory
        ai_memory.append(player1_move)
        if len(ai_memory) > 10:
            ai_memory.pop(0)
        session['ai_memory'] = ai_memory
    
    # Update score
    tuomari_data = session.get('tuomari', {
        'ekan_pisteet': 0,
        'tokan_pisteet': 0,
        'tasapelit': 0
    })
    
    result = ''
    if player1_move == player2_move:
        tuomari_data['tasapelit'] += 1
        result = 'Tasapeli!'
    elif (player1_move == 'k' and player2_move == 's') or \
         (player1_move == 's' and player2_move == 'p') or \
         (player1_move == 'p' and player2_move == 'k'):
        tuomari_data['ekan_pisteet'] += 1
        result = 'Pelaaja 1 voitti!'
    else:
        tuomari_data['tokan_pisteet'] += 1
        if game_mode == 'a':
            result = 'Pelaaja 2 voitti!'
        else:
            result = 'Tietokone voitti!'
    
    session['tuomari'] = tuomari_data
    
    # Add to history
    history = session.get('game_history', [])
    move_names = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
    history.append({
        'player1': move_names[player1_move],
        'player2': move_names[player2_move],
        'result': result
    })
    session['game_history'] = history
    
    return redirect(url_for('play'))


@app.route('/reset')
def reset():
    """Reset the game"""
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
