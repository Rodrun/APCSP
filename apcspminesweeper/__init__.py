from gym.envs.registration import register


register(
    id="apcsp-minesweeper-v0",
    entry_point="apcspminesweeper.envs:Minesweeper",
    kwargs={"rows": 9,
            "cols": 9,
            "w": 50}
)
