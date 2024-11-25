#![allow(unused)]


mod game;
mod piece;
mod board3;

use std::default::Default;
use macroquad::prelude::*;
use macroquad::window;
use game::Game;

#[macroquad::main("TROJAN STACKER GAME TRYOUTS")]
async fn main() {

    let mut game = Game::new();
    window::request_new_screen_size(800f32, 600f32);

    loop {
        clear_background(BLACK);

        handle_input(&mut game);

        render(&game);

        next_frame().await
    }
}

fn handle_input(game: &mut Game) {
    if is_key_pressed(KeyCode::Left) {
        game.move_cur_piece(-1);
    }
    if is_key_pressed(KeyCode::Right) {
        game.move_cur_piece(1);
    }
    if is_key_pressed(KeyCode::Space) {
        game.place_piece();
    }
    if is_key_pressed(KeyCode::Z) {
        game.rotate_ccw();
    }
    if is_key_pressed(KeyCode::X) {
        game.rotate_cw();
    }
    if is_key_pressed(KeyCode::C) || is_key_pressed(KeyCode::LeftShift) {
        game.hold_piece();
    }
}

fn render(game: &Game) {
    let basex = 10;
    let basey = 100;
    let sq_dim = 20;
    let thiccness = 1;
    for r in 0..20 {
        for c in 0..10 {
            let x = (basex + c*sq_dim) as f32;
            let y = (basey + r*sq_dim) as f32;
            draw_rectangle(x, y, sq_dim as f32, sq_dim as f32, game.get_board_tile(r, c).color());
            draw_rectangle_lines(x, y, sq_dim as f32, sq_dim as f32, thiccness as f32, WHITE);
        }
    }

    // Render current piece
    let cpbasex = basex;
    let cpbasey = 10;
    let draw_table = game.get_cur_piece().draw_table();
    let color = game.get_cur_piece().piece_type.color();
    let col = game.get_cur_piece().col;
    for r in 0..4 {
        for c in 0..4 {
            if draw_table[r*4 + c] {
                let x = (cpbasex + (c as i32)*sq_dim + col*sq_dim) as f32;
                let y = (cpbasey + (r as i32)*sq_dim) as f32;
                draw_rectangle(x+1.0, y+1.0, (sq_dim-1) as f32, (sq_dim-1) as f32, color);
            }
        }
    }

    // Instructions
    let inst_basex = basex + sq_dim*10 + 20;
    let inst_basey = basey;
    let font_size = 24.0;
    let instructions = [
        "Arrow left/right",
        "   to move",
        "Z/X to rotate",
        "Space to place",
        "C to hold",
        "",
        "Holding:"
    ];
    let mut y: f32 = inst_basey as f32;
    for inst in instructions {
        draw_text(inst, inst_basex as f32, y, font_size, WHITE);
        y += font_size + 2.0;
    }

    // Held piece
    draw_rectangle(inst_basex as f32, y, sq_dim as f32, sq_dim as f32, game.get_held_piece().color());
    draw_rectangle_lines(inst_basex as f32, y, sq_dim as f32, sq_dim as f32, thiccness as f32, WHITE);

    // Flag
    if game.condition_met() {
        let params = TextParams {
            font_size: font_size as u16,
            color: WHITE,
            ..Default::default()
        };
        draw_text_ex(&format!("CYBORG{{{}}}", game.piece_history)[..], basex as f32, (basey + 20*sq_dim + 20) as f32, params);
    }

}