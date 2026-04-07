from ir.program import Program


def validate_placement(program: Program) -> None:
    # TO-DO: add shim, comp and mem tile placement validations
    device = program.device
    seen_coords: set[tuple[int, int]] = set()

    for tile in program.tiles:
        if not device.contains(tile.col, tile.row):
            raise ValueError(
                f"Tile '{tile.name}' at ({tile.col}, {tile.row}) is outside device {device}"
            )

        coord = (tile.col, tile.row)
        if coord in seen_coords:
            raise ValueError(
                f"Multiple tiles occupy the same coordinate ({tile.col}, {tile.row})"
            )
        seen_coords.add(coord)