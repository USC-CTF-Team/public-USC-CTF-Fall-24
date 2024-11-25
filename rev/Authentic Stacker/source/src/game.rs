
use std::collections::VecDeque;
use macroquad::math::clamp;
use crate::piece::*;
use crate::board3::*;

const BOARD_WIDTH: i32 = 10;
const BOARD_HEIGHT: i32 = 20;
const INIT_COL: i32 = 3;
const BAG_ORDER: &str = "ISLJTZOLJISOTZLJZTIOSTOSJLIZTLJZIOSIJZSLTOITZOJLSJOLSIZTTLZISJOSOILTZJ";

pub struct Game {
    board: [Piece; 200],
    board2: [u8; 200],
    pieces: VecDeque<Piece>,
    hold: Piece,
    cur_piece: PieceInfo,
    pieces_placed: i32,
    pub piece_history: String
}

impl Game {
    pub fn new() -> Game {
        let mut bag = VecDeque::new();
        for c in BAG_ORDER.chars() {
            bag.push_back(Piece::from_char(c));
        }
        let mut g = Game {
            board: [Piece::None; 200],
            board2: [0; 200],
            pieces: bag,
            hold: Piece::None,
            cur_piece: PieceInfo { piece_type: Piece::None, rot: Rotation::None, col: 0},
            pieces_placed: 0,
            piece_history: String::new()
        };
        g.set_next_piece();
        g
    }

    pub fn get_board_tile(&self, row: i32, col: i32) -> Piece {
        if (row < 0 || row >= BOARD_HEIGHT || col < 0 || col >= BOARD_WIDTH) {
            panic!("out of bounds");
        }
        self.board[(row * BOARD_WIDTH + col) as usize]
    }

    pub fn set_board_tile(&mut self, row: i32, col: i32, piece: Piece) {
        if (row < 0 || row >= BOARD_HEIGHT || col < 0 || col >= BOARD_WIDTH) {
            panic!("out of bounds");
        }
        self.board[(row * BOARD_WIDTH + col) as usize] = piece;
        self.board2[(row * BOARD_WIDTH + col) as usize] = self.pieces_placed as u8;
    }

    pub fn move_cur_piece(&mut self, delta: i32) {
        self.cur_piece.col = clamp(self.cur_piece.col + delta, 0, BOARD_WIDTH - self.cur_piece.width());
    }

    pub fn get_cur_piece(&self) -> &PieceInfo {
        &self.cur_piece
    }

    pub fn rotate_cw(&mut self) {
        self.cur_piece.rot = match &self.cur_piece.rot {
            Rotation::None => Rotation::CW,
            Rotation::CW => Rotation::Half,
            Rotation::Half => Rotation::CCW,
            Rotation::CCW => Rotation::None
        };
        self.move_cur_piece(0);
    }

    pub fn rotate_ccw(&mut self) {
        self.cur_piece.rot = match &self.cur_piece.rot {
            Rotation::None => Rotation::CCW,
            Rotation::CCW => Rotation::Half,
            Rotation::Half => Rotation::CW,
            Rotation::CW => Rotation::None
        };
        self.move_cur_piece(0);
    }

    pub fn place_piece(&mut self) {
        let mut best_y = None;
        let col = self.cur_piece.col;
        let table = self.cur_piece.draw_table();
        for y in (0..=(20 - self.cur_piece.height())) {
            let mut valid = true;
            'piece:
            for pr in 0..4 {
                for pc in 0..4 {
                    if table[pr*4 + pc] && self.get_board_tile(y+(pr as i32), col+(pc as i32)) != Piece::None {
                        valid = false;
                        break 'piece;
                    }
                }
            }
            if !valid { break; }
            else { best_y = Some(y); }
        }

        if best_y.is_some() {
            self.pieces_placed += 1;
            if self.pieces_placed > 1 { self.piece_history += "_"; }
            self.piece_history.push_str(&self.cur_piece.id());
            for pr in 0..4 {
                for pc in 0..4 {
                    if table[pr * 4 + pc] {
                        self.set_board_tile(best_y.unwrap() + (pr as i32), col + (pc as i32), self.cur_piece.piece_type);
                    }
                }
            }
            self.set_next_piece();
        }
    }

    pub fn set_next_piece(&mut self) {
        self.cur_piece = PieceInfo { piece_type: self.pieces.pop_front().unwrap_or(Piece::None), col: INIT_COL, rot: Rotation::None};
    }

    pub fn hold_piece(&mut self) {
        if self.hold == Piece::None {
            self.hold = self.cur_piece.piece_type;
            self.set_next_piece();
        }
        else {
            let temp = self.hold;
            self.hold = self.cur_piece.piece_type;
            self.cur_piece = PieceInfo { piece_type: temp, col: INIT_COL, rot: Rotation::None };
        }
    }

    pub fn get_held_piece(&self) -> Piece {
        self.hold
    }

    pub fn condition_met(&self) -> bool {
        self.board2 == BOARD3
    }
}