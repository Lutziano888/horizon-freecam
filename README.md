# Freecam (Horizon native mod)

Press **F4** to leave your body and fly the camera freely while your player stays where it is. Press **F4** again to
snap back. In **fair play** mode the camera can't fly through blocks.

| Key | What it does while flying |
|---|---|
| W A S D | Fly where you look |
| Space / Shift | Up / down |
| Ctrl | 2.5x faster |
| Mouse wheel | Change the speed (0.1x to 10x) |

Options > Mods > Freecam has the key and three settings:

- **Speed**: 2, 5, 10, 20, 40 or 80 blocks a second.
- **Fair play** (off by default): the camera is a small box (0.6 blocks) that can't pass through blocks, using the
  blocks' real collision shapes: glass, fences and doors stop it, grass and flowers don't. No looking into caves or
  bases through walls; the camera stops at a wall and slides along it.
- **Allowed on servers** (on by default; in your own worlds it always works). Some servers don't allow freecam:
  check their rules.

While the camera flies, your player stands still, doesn't attack, mine or use items, and you see its body from
outside. The world only shows the chunks loaded around your player.

## Install

In the Horizon launcher: Mods → Freecam → Install, then build the game with your native mods (Settings → Game →
Native mods). The launcher downloads its own Rust and builds Horizon with the mod; see Horizon's
[native mods](https://github.com/horizon-rust/horizon/blob/main/docs/native-mods.md). Native mods run with the
game's full access to your computer: install them only from authors you trust.

## How it works

It is a [horizon-mixins](https://github.com/horizon-rust/horizon-mixins) bundle (`mixins/freecam/`) that the
launcher builds into the game:

| Hook | Where | What it does |
|---|---|---|
| `native_key`, `native_wheel`, `native_tick`, `native_mods`, `native_settings`, `native_settings_click` | Horizon's native hook points | The key, the wheel, giving the movement keys back after the tick, the Options > Mods row and settings |
| `camera_view` (cancellable HEAD) | `game/perspective.rs` | The world is drawn from the free camera; in fair play it is kept out of blocks with `can_dismount_to` |
| `turn_player` (cancellable HEAD) | `game/perspective.rs` | The mouse turns the camera, not the player |
| `own_body_in_view` (cancellable HEAD) | `game/perspective.rs` | The player's body is drawn |
| `hand_geometry` (cancellable HEAD) | `game.rs` | No first-person hand |
| `tick_remote_level` (HEAD) | `game/remote.rs` | The movement keys are held back from the player's tick |
| `key_pressed`, `play_mouse` (cancellable HEAD) | `game.rs` | No jumping, sneaking, attacking or using while flying |

The camera, turning and the player's tick are not Horizon's stable hook points, so the bundle is **pinned** to the
Horizon commit in `compatibility.json`. When Horizon changes those functions, the mod needs a new release on a newer
commit (the launcher's "Build anyway" often still works in between).

| File | What it is |
|---|---|
| `mixins/freecam/horizon-mixin.toml` | The bundle: one module and the HEAD hooks |
| `mixins/freecam/runtime.rs` | The mod's logic and state (`game::freecam` in the game); also this crate's library, for its tests |
| `mixins/freecam/*.rs` | One small helper per hook |
| `tools/package.py` | Packages `target/freecam-<version>.hnmod` for a release |

## Build and check

```sh
cargo test                                   # the logic: settings, flying, fair play, turning, the wheel
horizon-mixins apply --workspace ../horizon --mods mixins --out ../stage   # Horizon at the pinned commit
(cd ../stage && cargo check --locked -p horizon-client --bin horizon-client)
python3 tools/package.py                     # target/freecam-1.1.0.hnmod
```

`horizon-mixins` refuses symbolic links in the workspace: export Horizon at the pinned commit
(`git archive`) rather than pointing it at a checkout with links.

License: MIT.
