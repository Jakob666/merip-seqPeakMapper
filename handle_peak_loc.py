# -*- coding:utf-8 -*-
import pandas as pd


element_priority = {"stop_codon": 1, "three_prime_utr": 2, "CDS": 3, "five_prime_utr": 4}

data = pd.read_csv("/data/nanopore/merip_seq_data/metpeak_calling_res/peak_location/peak_loc.tsv", sep="\t", header=None)
data.columns = ["chr", "strand", "start", "end", "center", "element", "element start", "element end"]

data["priority"] = 0

get_priority = lambda record: element_priority[record["element"]]

data["priority"] = data.apply(get_priority, axis=1)

data.sort_values(by=["chr", "strand", "start", "end", "priority"], ascending=True, inplace=True)
data.drop_duplicates(subset=["chr", "strand", "start", "end", "priority"], keep="first", inplace=True)
data.to_csv("/data/nanopore/merip_seq_data/metpeak_calling_res/peak_location/peak_unique_loc.tsv", sep="\t", index=False)
