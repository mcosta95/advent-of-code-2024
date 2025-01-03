def main_code(file_name, part=1):
    disk_map = read_txt_to_str(file_name, with_split=None)

    pairs_combination = zip_longest(*[iter(disk_map)]*2, fillvalue="")
    pairs_blocks_free_space = [(a, b) for a, b in pairs_combination if a]

    check_sum = 0
    curr_index = 0
    last_idx = -1
    idx_ = 0
    max_idx = len(pairs_blocks_free_space)-1

    while idx_ <= max_idx:
    
        file_, free_space = pairs_blocks_free_space[idx_]
        block_file = int(file_)
        free_space = int(free_space)

        print(f"ID: {idx_} with block file {block_file}, let's fill the free space {free_space}")

        # calculate the block_number
        check_sum += calculate_block_score(curr_index, block_file, idx_)
        print(f"Current score block: {check_sum}")
        curr_index += block_file


        curr_free_space = free_space
        # iterate until no free space on the block
        while curr_free_space!=0 and idx_<max_idx:
            idx_last_block, last_block = fetch_last_block(pairs_blocks_free_space, last_idx=last_idx)

            

            if idx_last_block:
                # lets see how much free space we have to fill
                max_range = curr_index+curr_free_space
                if last_block<=curr_free_space:
                    max_range = curr_index+last_block
                else:
                    # update pairs_blocks_free_space
                    pairs_blocks_free_space[last_idx] = (str(last_block-curr_free_space), pairs_blocks_free_space[last_idx][1])

                check_sum += sum(i * idx_last_block for i in range(curr_index, max_range))
                print(f"Current score free space: {check_sum}")

                curr_index = max_range
                last_idx = last_idx+(-1) if last_block-curr_free_space <= 0 else last_idx
                max_idx = max_idx-1 if last_block-curr_free_space <= 0 else max_idx
                curr_free_space = 0 if curr_free_space - last_block <= 0 else curr_free_space - last_block

        idx_+=1
                