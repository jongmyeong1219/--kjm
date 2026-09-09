import streamlit as st
import chess
import chess.svg
import base64
from stockfish import Stockfish

# -----------------------------------------------------------------------------
# 1. 오프닝 데이터베이스 (전문적이고 검증된 주요 수순)
# -----------------------------------------------------------------------------
OPENINGS = {
    "이탈리안 게임 (Italian Game)": {
        "지우코 피아노 (Giuoco Piano)": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5", "c2c3", "g8f6", "d2d3"],
            "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d3",
            "desc": "견고하고 정통적인 센터 지배 및 기물 배치 오프닝입니다."
        },
        "프라이드 리버 어택 (Fried Liver Attack)": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6", "f3g5", "d7d5", "e4d5", "f6d5", "g5f7"],
            "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. Ng5 d5 5. exd5 Nxd5 6. Nxf7!",
            "desc": "흑의 f7 지점을 미끼와 기물 희생으로 공격하는 매우 날카로운 전술 오프닝입니다."
        },
        "에반스 갬빗 (Evans Gambit)": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5", "b2b4", "c5b4", "c2c3", "b4a5"],
            "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. b4 Bxb4 5. c3 Ba5",
            "desc": "b폰을 희생하여 빠르게 중앙을 장악하고 템포를 빼앗는 공격적 갬빗입니다."
        }
    },
    "시실리안 디펜스 (Sicilian Defense)": {
        "나이돌프 바리에이션 (Najdorf Variation)": {
            "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "a7a6"],
            "pgn": "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6",
            "desc": "그랜드마스터들이 가장 많이 사용하는 카운터 공격 오프닝입니다."
        },
        "드래곤 바리에이션 (Dragon Variation)": {
            "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "g7g6"],
            "pgn": "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 g6",
            "desc": "비숍을 g7에 피앙케토하여 대각선을 강력하게 지배하는 동적인 바리에이션입니다."
        },
        "알라핀 바리에이션 (Alapin Variation)": {
            "moves": ["e2e4", "c7c5", "c2c3", "g8f6", "e4e5", "f6d5", "d2d4"],
            "pgn": "1. e4 c5 2. c3 Nf6 3. e5 Nd5 4. d4",
            "desc": "복잡한 메인 라인을 피하고 빠르게 d4 중앙 파급력을 형성하는 수입니다."
        }
    },
    "루이 로페즈 (Ruy Lopez / Spanish Game)": {
        "모피 디펜스 (Morphy Defense)": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6", "b5a4", "g8f6", "e1g1"],
            "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O",
            "desc": "루이 로페즈의 가장 대표적이고 정석적인 수순입니다."
        },
        "베를린 디펜스 (Berlin Defense)": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "g8f6", "e1g1", "f6e4", "d2d4"],
            "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. O-O Nxe4 5. d4",
            "desc": "'베를린 장벽'이라 불릴 정도로 철벽 수비를 자랑하는 수순입니다."
        },
        "익스체인지 바리에이션 (Exchange Variation)": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6", "b5c6", "d7c6"],
            "pgn": "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Bxc6 dxc6",
            "desc": "3번째 수에서 즉시 나이트를 교환하여 흑의 폰 구조를 무너뜨리는 전략입니다."
        }
    }
}

# -----------------------------------------------------------------------------
# 2. 헬퍼 함수
# -----------------------------------------------------------------------------
def render_svg(board):
    """체스 판을 SVG로 변환하여 HTML로 출력"""
    svg_board = chess.svg.board(board=board, size=400)
    b64 = base64.b64encode(svg_board.encode('utf-8')).decode('utf-8')
    return f'<img src="data:image/svg+xml;base64,{b64}"/>'

# -----------------------------------------------------------------------------
# 3. Streamlit 앱 메인 UI
# -----------------------------------------------------------------------------
st.set_page_config(page_title="체스 오프닝 마스터 & AI 대진", layout="wide")
st.title("♟️ 체스 오프닝 학습 & AI 실전 대진 플랫폼")

# 탭 구성
tab1, tab2 = st.tabs(["📚 오프닝 직접 연습하기", "🤖 AI 대진 (Rating 400~2800)"])

# =============================================================================
# TAB 1: 오프닝 직접 연습하기
# =============================================================================
with tab1:
    st.header("오프닝 수순 학습 및 실습")
    
    col_select1, col_select2 = st.columns(2)
    with col_select1:
        category = st.selectbox("오프닝 카테고리 선택", list(OPENINGS.keys()))
    with col_select2:
        variation = st.selectbox("바리에이션 선택", list(OPENINGS[category].keys()))
        
    selected_data = OPENINGS[category][variation]
    st.subheader(f"📖 {variation}")
    st.info(f"**PGN**: `{selected_data['pgn']}`\n\n**설명**: {selected_data['desc']}")

    # 세션 상태 초기화
    if "study_board" not in st.session_state or st.session_state.get("current_var") != variation:
        st.session_state.study_board = chess.Board()
        st.session_state.move_step = 0
        st.session_state.current_var = variation

    board = st.session_state.study_board
    target_moves = selected_data["moves"]

    col_board, col_ctrl = st.columns([1, 1])
    
    with col_board:
        st.markdown(render_svg(board), unsafe_allow_html=True)

    with col_ctrl:
        st.write(f"### 진행 상황 ({st.session_state.move_step} / {len(target_moves)} 수)")
        
        if st.session_state.move_step < len(target_moves):
            next_move_uci = target_moves[st.session_state.move_step]
            move_obj = chess.Move.from_uci(next_move_uci)
            next_san = board.san(move_obj)
            
            st.write(f"👉 **다음 추천 수**: `{next_san}` (UCI: `{next_move_uci}`)")
            
            user_move = st.text_input("수를 입력하세요 (예: e2e4 또는 e4)", key=f"input_{st.session_state.move_step}")
            
            if st.button("수 두기"):
                try:
                    # SAN 또는 UCI 입력 자동 처리
                    try:
                        parsed_move = board.parse_san(user_move)
                    except ValueError:
                        parsed_move = chess.Move.from_uci(user_move)

                    if parsed_move == move_obj:
                        board.push(parsed_move)
                        st.session_state.move_step += 1
                        st.success("정답입니다!")
                        st.rerun()
                    else:
                        st.error("정확한 오프닝 수순이 아닙니다. 다시 시도해 보세요!")
                except Exception:
                    st.error("올바른 수 형식이 아닙니다 (예: e2e4, Nf3, e4 등).")
        else:
            st.balloons()
            st.success("🎉 해당 오프닝 바리에이션 수순 학습을 완료했습니다!")

        if st.button("처음부터 다시 시도"):
            st.session_state.study_board = chess.Board()
            st.session_state.move_step = 0
            st.rerun()

# =============================================================================
# TAB 2: AI 대진
# =============================================================================
with tab2:
    st.header("🤖 AI 상대 대진 (Stockfish 엔진)")
    
    # Stockfish 경로 지정 (다운로드받은 스톡피쉬 파일 경로로 설정)
    # 예: Windows -> "C:/stockfish/stockfish-windows-x86-64-avx2.exe"
    # 예: Linux/Mac -> "/usr/local/bin/stockfish" 또는 "./stockfish"
    STOCKFISH_PATH = "C:/stockfish/stockfish-windows-x86-64-avx2.exe" 

    col_ai_cfg1, col_ai_cfg2 = st.columns(2)
    with col_ai_cfg1:
        user_color = st.radio("플레이할 색상 선택", ["백 (White)", "흑 (Black)"])
    with col_ai_cfg2:
        ai_rating = st.slider("AI 레이팅 (Elo)", min_value=400, max_value=2800, value=1200, step=100)

    # 게임 세션 초기화
    if "ai_board" not in st.session_state:
        st.session_state.ai_board = chess.Board()

    ai_board = st.session_state.ai_board
    is_user_white = user_color.startswith("백")

    col_play_board, col_play_ctrl = st.columns([1, 1])

    with col_play_board:
        st.markdown(render_svg(ai_board), unsafe_allow_html=True)

    with col_play_ctrl:
        st.write(f"**상대 AI 난이도**: Elo {ai_rating}")
        
        if ai_board.is_game_over():
            st.error(f"게임 종료! 결과: {ai_board.result()}")
        else:
            # 유저의 차례인지 확인
            is_user_turn = (ai_board.turn == chess.WHITE and is_user_white) or (ai_board.turn == chess.BLACK and not is_user_white)
            
            if is_user_turn:
                play_move = st.text_input("착수 입력 (예: e2e4, Nf3, O-O)", key="game_move_input")
                if st.button("수 두기", key="game_move_btn"):
                    try:
                        move = ai_board.parse_san(play_move)
                        if move in ai_board.legal_moves:
                            ai_board.push(move)
                            st.rerun()
                        else:
                            st.warning("합법적인 수가 아닙니다.")
                    except ValueError:
                        try:
                            move = chess.Move.from_uci(play_move)
                            if move in ai_board.legal_moves:
                                ai_board.push(move)
                                st.rerun()
                            else:
                                st.warning("합법적인 수가 아닙니다.")
                        except Exception:
                            st.error("올바른 수 입력 형식이 아닙니다.")
            else:
                st.info("AI가 수를 계산 중입니다...")
                if st.button("AI 착수 요청"):
                    try:
                        sf = Stockfish(path=STOCKFISH_PATH)
                        sf.set_elo_rating(ai_rating)
                        sf.set_fen_position(ai_board.fen())
                        
                        best_move = sf.get_best_move()
                        if best_move:
                            ai_board.push(chess.Move.from_uci(best_move))
                            st.rerun()
                    except Exception as e:
                        st.error(f"Stockfish 엔진 실행 오류: {e}\n`STOCKFISH_PATH` 경로가 올바른지 확인해주세요.")

        if st.button("새 게임 시작"):
            st.session_state.ai_board = chess.Board()
            st.rerun()
