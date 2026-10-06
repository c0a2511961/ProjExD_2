import math
import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数: 描画先のScreen Surface
    戻り値: なし
    """
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.set_alpha(150)
    black_sfc.fill((0, 0, 0))
    screen.blit(black_sfc, [0, 0])

    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)

    left_kk_rct = crying_kk_img.get_rect()
    left_kk_rct.center = WIDTH // 2 - 200, HEIGHT // 2
    screen.blit(crying_kk_img, left_kk_rct)

    right_kk_rct = crying_kk_img.get_rect()
    right_kk_rct.center = WIDTH // 2 + 200, HEIGHT // 2
    screen.blit(crying_kk_img, right_kk_rct)

    font = pg.font.Font(None, 80)
    txt_sfc = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_sfc.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    screen.blit(txt_sfc, txt_rct)

    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    段階的に拡大・加速するための爆弾Surfaceリストと加速度リストを生成する関数
    引数: なし
    戻り値: 爆弾Surfaceのリスト, 加速度のリスト
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs    

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量に応じたこうかとん画像の辞書を生成する関数
    引数: なし
    戻り値: 移動量タプルをキー、回転・反転したこうかとんSurfaceを値とする辞書
    """
    base_img = pg.image.load("fig/3.png")
    flipped_img = pg.transform.flip(base_img, True, False)

    return {
        (0, 0): pg.transform.rotozoom(base_img, 0, 0.9),
        (-5, 0): pg.transform.rotozoom(base_img, 0, 0.9),
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),
        (0, -5): pg.transform.rotozoom(flipped_img, 90, 0.9),
        (+5, -5): pg.transform.rotozoom(flipped_img, 45, 0.9),
        (+5, 0): pg.transform.rotozoom(flipped_img, 0, 0.9),
        (+5, +5): pg.transform.rotozoom(flipped_img, -45, 0.9),
        (0, +5): pg.transform.rotozoom(flipped_img, -90, 0.9),
        (-5, +5): pg.transform.rotozoom(base_img, 45, 0.9),
    }

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10)  
    vx, vy = +5, +5  

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if not check_bound(kk_rct)[0] or not check_bound(kk_rct)[1]:
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = kk_imgs.get(tuple(sum_mv), kk_imgs[(0, 0)])
        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        acc = bb_accs[idx]
        avx = vx * acc
        avy = vy * acc

        bb_img = bb_imgs[idx]
        bb_rct.width = bb_img.get_width()
        bb_rct.height = bb_img.get_height()

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  
            vx *= -1
        if not tate:  
            vy *= -1  
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
