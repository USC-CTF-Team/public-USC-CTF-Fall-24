use macroquad::color::*;
use macroquad::color_u8;

#[derive(Copy, Clone, Eq, PartialEq)]
pub enum Piece { None, T, S, Z, L, J, I, O }

impl Piece {
    pub fn from_char(c: char) -> Piece {
        match c {
            'T' => Piece::T,
            'S' => Piece::S,
            'Z' => Piece::Z,
            'L' => Piece::L,
            'J' => Piece::J,
            'I' => Piece::I,
            'O' => Piece::O,
            _ => Piece::None
        }
    }
    pub fn color(&self) -> Color {
        match &self {
            Piece::None => BLACK,
            Piece::T => PURPLE,
            Piece::S => LIME,
            Piece::Z => RED,
            Piece::L => ORANGE,
            Piece::J => BLUE,
            Piece::I => SKYBLUE,
            Piece::O => YELLOW
        }
    }
}

pub enum Rotation { None, CW, Half, CCW }

pub struct PieceInfo {
    pub piece_type: Piece,
    pub rot: Rotation,
    pub col: i32
}

impl PieceInfo {
    pub fn width(&self) -> i32 {
        match (&self.piece_type, &self.rot) {
            (Piece::None, _) => 0,
            (Piece::T | Piece::S | Piece::Z | Piece::J | Piece::L, Rotation::None | Rotation::Half) => 3,
            (Piece::T | Piece::S | Piece::Z | Piece::J | Piece::L, Rotation::CW | Rotation::CCW) => 2,
            (Piece::O, _) => 2,
            (Piece::I, Rotation::None | Rotation::Half) => 4,
            (Piece::I, Rotation::CW | Rotation::CCW) => 1
        }
    }

    pub fn height(&self) -> i32 {
        match (&self.piece_type, &self.rot) {
            (Piece::None, _) => 0,
            (Piece::T | Piece::S | Piece::Z | Piece::J | Piece::L, Rotation::None | Rotation::Half) => 2,
            (Piece::T | Piece::S | Piece::Z | Piece::J | Piece::L, Rotation::CW | Rotation::CCW) => 3,
            (Piece::O, _) => 2,
            (Piece::I, Rotation::None | Rotation::Half) => 1,
            (Piece::I, Rotation::CW | Rotation::CCW) => 4
        }
    }

    pub fn id(&self) -> String {
        let mut s = String::new();
        s += match &self.piece_type {
            Piece::None => "?",
            Piece::T => "t",
            Piece::S => "s",
            Piece::Z => "z",
            Piece::L => "L",
            Piece::J => "j",
            Piece::I => "i",
            Piece::O => "o"
        };
        s += match &self.piece_type {
            Piece::T | Piece::L | Piece::J => match &self.rot {
                Rotation::None => "0",
                Rotation::CW => "1",
                Rotation::Half => "2",
                Rotation::CCW => "3"
            },
            Piece::S | Piece::Z | Piece::I => match &self.rot {
                Rotation::None | Rotation::Half => "0",
                Rotation::CW | Rotation::CCW => "1"
            },
            Piece::O => "0",
            Piece::None => "?"
        };
        s += &self.col.to_string();
        s
    }

    pub fn draw_table(&self) -> [bool; 16] {
        const X: bool = true;
        const O: bool = false;
        match &self.piece_type {
            Piece::None => [false; 16],
            Piece::T => match &self.rot {
                Rotation::None => [
                    X,X,X,O,
                    O,X,O,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CW => [
                    O,X,O,O,
                    X,X,O,O,
                    O,X,O,O,
                    O,O,O,O
                ],
                Rotation::Half => [
                    O,X,O,O,
                    X,X,X,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CCW => [
                    X,O,O,O,
                    X,X,O,O,
                    X,O,O,O,
                    O,O,O,O
                ],
            }
            Piece::S => match &self.rot {
                Rotation::None | Rotation::Half => [
                    X,X,O,O,
                    O,X,X,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CW | Rotation::CCW => [
                    O,X,O,O,
                    X,X,O,O,
                    X,O,O,O,
                    O,O,O,O
                ]
            }
            Piece::Z => match &self.rot {
                Rotation::None | Rotation::Half => [
                    O,X,X,O,
                    X,X,O,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CW | Rotation::CCW => [
                    X,O,O,O,
                    X,X,O,O,
                    O,X,O,O,
                    O,O,O,O
                ]
            }
            Piece::L => match &self.rot {
                Rotation::None => [
                    O,O,X,O,
                    X,X,X,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CW => [
                    X,O,O,O,
                    X,O,O,O,
                    X,X,O,O,
                    O,O,O,O
                ],
                Rotation::Half => [
                    X,X,X,O,
                    X,O,O,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CCW => [
                    X,X,O,O,
                    O,X,O,O,
                    O,X,O,O,
                    O,O,O,O
                ]
            }
            Piece::J => match &self.rot {
                Rotation::None => [
                    X,O,O,O,
                    X,X,X,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CW => [
                    X,X,O,O,
                    X,O,O,O,
                    X,O,O,O,
                    O,O,O,O
                ],
                Rotation::Half => [
                    X,X,X,O,
                    O,O,X,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CCW => [
                    O,X,O,O,
                    O,X,O,O,
                    X,X,O,O,
                    O,O,O,O
                ]
            }
            Piece::I => match &self.rot {
                Rotation::None | Rotation::Half => [
                    X,X,X,X,
                    O,O,O,O,
                    O,O,O,O,
                    O,O,O,O
                ],
                Rotation::CW | Rotation::CCW => [
                    X,O,O,O,
                    X,O,O,O,
                    X,O,O,O,
                    X,O,O,O
                ]
            }
            Piece::O => [
                X,X,O,O,
                X,X,O,O,
                O,O,O,O,
                O,O,O,O
            ]
        }
    }
}

