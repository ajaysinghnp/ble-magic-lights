# commands.py

COMMANDS = {
    # Power
    "turn_on": bytes.fromhex("bf01b05ee288275b1f3e64d8d47d85af1a"),
    "turn_on_2": bytes.fromhex("7b4a63877358d460209079bc0190def30f"),
    "turn_on_3": bytes.fromhex("360742cfd536319078bc0190def3b53731"),
    "turn_off": bytes.fromhex("c060011068201190def3b5375b1e3e6435"),
    "turn_off_2": bytes.fromhex("ac7da52f8a304e9278024a4307624fc486"),
    "turn_off_3": bytes.fromhex("acd45d05be343e5e9278024a4307624f05"),
    # Static colors
    "static_red": bytes.fromhex("a79b0ede83e0204abc07624fc4602190c9"),
    "static_green": bytes.fromhex("d7f395b74a191c64d82b7d85af9b2e5e3d"),
    "static_blue": bytes.fromhex("0b90fe73a418791e3e6427d47d85af9b1b"),
    "static_light_blue": bytes.fromhex("0f90fe73a43b791e7ea027d47d85af9b7b"),
    "static_white_low": bytes.fromhex("f5b517db0fd554d8d47d85af9b2e5e927e"),
    "static_white_high": bytes.fromhex("a49b0ede83fb204abcf89d4fc4602190e9"),
    "static_light_yellow": bytes.fromhex("ae01b05ee2bf155be19524d8d47d85af7a"),
    "static_yellow_green": bytes.fromhex("3264f8546c018d9bd1a19278024a4307e3"),
    "static_light_green": bytes.fromhex("474327e25e5542216f86bc0190def3b530"),
    "static_light_white": bytes.fromhex("77026ac316986dc49f73c279bc0190de2e"),
    "static_white_green": bytes.fromhex("827822ca523c404f3b8b1a9079bc0190ad"),
    "static_light_sky_blue_high": bytes.fromhex("5d90fe73a44a0e1e3eb9d8097d85af9bbb"),
    "static_light_green_low": bytes.fromhex("a460011068885490def3d3375b1e3e6455"),
    "static_purple_low": bytes.fromhex("d1377b9e2f298dd47d5d77432e5e9278ff"),
    "static_warm_medium": bytes.fromhex("3521b0f9adb5c5def3b59f5b1e3e64d896"),
    # Gradients / Effects
    "seven_color_gradient": bytes.fromhex("0d3e4458c5c89cafbcd1a16d78464a43c2"),
    "seven_color_gradient_high_speed": bytes.fromhex(
        "164a638773dfdd60066f8643019ddef34f"
    ),
    "seven_color_gradient_low": bytes.fromhex("5f4327e25e064321aa79bc0190def3b5d0"),
    "three_color_gradient": bytes.fromhex("b69b0ede83b0214abc07624fc4602190c9"),
    "green_gradient": bytes.fromhex("514327e25e5e7921b079430190cff3b530"),
    "blue_strobe": bytes.fromhex("c5d45d05be8d375ed27802b54316624fa5"),
    "white_flow_high_speed": bytes.fromhex("1c4a63541e0cd76023908643fe6f21f32f"),
    "blue_on_purple_flow_high_speed": bytes.fromhex(
        "7bd8f42ef964882e5c928702b543f89d44"
    ),
    "blue_flow_high_speed": bytes.fromhex("7b1e1e37a4306e85ad9a2ea16d7802b541"),
    "purple_on_blue_high_speed": bytes.fromhex("6207421cb8b432907bbc0190210cb5c811"),
    "yellow_on_blue_high_speed": bytes.fromhex("b2799c52ece0e0b5355b1e3e9b272b7df8"),
    "green_on_blue_high_speed": bytes.fromhex("6cc44072eca8af0192def3b5c85be13e54"),
    "green_on_blue_high_speed_rev": bytes.fromhex("524fe4335d4e6abc0391def34a37a41e93"),
    "red_on_blue_high_speed": bytes.fromhex("b4ded3e64b870d3e66d8d47d7a509b2edc"),
    "white_on_green_high_speed": bytes.fromhex("274a63541e98d76023907943016f210cef"),
    "yellow_on_white_high_speed_rev": bytes.fromhex(
        "a3afbb7d222e6b024843f89db03b9f21e8"
    ),
    "multi_on_purple_high_speed": bytes.fromhex("6d432731339c732191783c0110def3b510"),
    "green_on_red_high_speed": bytes.fromhex("879b0e0deee8114a41079d4fc460de90e9"),
    "green_on_red_high_speed_rev": bytes.fromhex("54858fc852dd8178004bbc0762b03b60a7"),
    "white_on_green_high_speed_rev": bytes.fromhex(
        "b62e7ec1047e594305634f3b60216f86aa"
    ),
    "white_on_green_high_speed_high": bytes.fromhex(
        "56bc21c3a257a637591e3e9bd82b827ad9"
    ),
    "light_green_flow": bytes.fromhex("504fe4335dda6abc0391210cb537a41eb3"),
    "light_blue_flow_rev": bytes.fromhex("0b64f8870168bc9b2c5f9287fd4a43f8c3"),
    "purple_flow_high": bytes.fromhex("efd45dd6d3f23d5e9078fd4abcf8624f05"),
    "multi_on_red_rev": bytes.fromhex("76432731330d732191783c0190def3b550"),
    "multi_on_red": bytes.fromhex("77432731331f73219179bc0110def3b5d0"),
}
