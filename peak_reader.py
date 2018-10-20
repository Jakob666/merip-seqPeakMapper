# -*- coding:utf-8 -*-
"""
@author: hbs
@date: 2018-10-19
Description:
    Load and extract useful informations from the BED format output file of peak calling software, such as MACS and
    MeTPeak etc.
"""
import pandas as pd


class PeakReader:
    """
    handling for bed format file generated by MeTPeak、MACS etc.
    """
    def __init__(self, peak_file):
        self.peak_file = peak_file
        self.peaks = []

    def peak_info(self):
        """
        extract peak information from bed format file.
        :return:
        """
        with open(self.peak_file, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                info = line.split("\t")
                if len(info) >= 10:
                    try:
                        chr_num, start, end, strand, peak_center, peak_length = PeakReader.peak_with_block(info)
                    except:
                        print(line)
                        exit()
                else:
                    chr_num, start, end, strand, peak_center, peak_length = PeakReader.peak_without_block(info)
                self.peaks.append([chr_num, start, end, strand, peak_center, peak_length])
        self.peaks = pd.DataFrame(self.peaks, columns=["chr", "start", "end", "strand", "peak_center", "peak_length"])
        return None

    @staticmethod
    def peak_with_block(info):
        """
        bed file has at least 10 columns, if the number in the teenth column is greater than 1 represent that blocks
        exist in this area.
        :return:
        """
        chr_num, start, end, strand, count, block_size, block_start = info[0], int(info[1]), info[2], info[5], info[-3], info[-2], info[-1]
        if int(count) > 1:
            sizes = list(map(int, block_size.split(",")[:-1]))
            start_sites = list(map(int, block_start.split(",")))
            peak_length = sum(sizes)
            if sizes[0] > peak_length // 2 + 1:
                peak_center = start + peak_length // 2 + 1
            else:
                for i in range(1, len(sizes)):
                    if sum(sizes[:i]) <= peak_length // 2 + 1 < sum(sizes[:i+1]):
                        peak_center = start + start_sites[i] + peak_length // 2 + 1 - sum(sizes[:i])
                        break
                    else:
                        continue

        else:
            block_size = block_size.split(",")[0]
            peak_length = int(block_size)
            peak_center = int(start) + peak_length // 2 + 1

        return chr_num, start, end, strand, peak_center, peak_length

    @staticmethod
    def peak_without_block(info):
        """
        bed file has less than 10 columns or the number in the teenth column equals 1 represent no existed blocks
        in this area.
        :return:
        """
        try:
            strand = info[5]
        except IndexError:
            strand = "+"

        chr_num, start, end = info[0], info[1], info[2]
        peak_length = end - start + 1
        peak_center = start + (start - end) // 2

        return chr_num, start, end, strand, peak_center, peak_length


if __name__ == "__main__":
    # just testing code
    pr = PeakReader("/data/nanopore/merip_seq_data/metpeak_calling_res/peak_location/reference_files/example.bed")
    pr.peak_info()
    print(pr.peaks.head(10))