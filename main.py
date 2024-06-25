# from Game import load_board_from_file, ParkingPuzzle, astar



# board = load_board_from_file('nivel.txt')
# puzzle = ParkingPuzzle(board)
# meta = puzzle.goal_position

# w1, w2, w3 = 1, 1, 1

# result = astar(puzzle, w1, w2, w3)
# if result:
#      with open("astar.txt", 'w+') as file:
#         file.writelines("Ultima corrida:")
#         for key, value in result.items():
#             if (key != "max_ram_usage" and key != "running_time"):
#                 file.write(f"{key}: {value}\n")
#             else:
#                 file.write(f"{key}: {value:.4f} \n")
# else:
#     print("No se encontró solución.")
