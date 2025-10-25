import openAIFunctions as f1

f1.client = f1.keyRead()

playersRaw = f1.analyzeImagePIL("../pic1.jpg")

print(playersRaw)
# if "3" in str(range(1, 11)):
#     print("yes")

# import test2 as b

# # f1.client = f1.keyRead()

# print(int("01"))
# for _ in range(10):
#     print(b.BotIrlBrain.readSave([5, 8]))

#     nums = b.BotIrlBrain.readSave([5, 8])

#     nums[0] = int(nums[0])
#     nums[1] = int(nums[1])

#     nums[0] = nums[1] if nums[0] >= nums[1] else nums[0] + 1

#     b.BotIrlBrain.writeSave([5], [nums[0]])