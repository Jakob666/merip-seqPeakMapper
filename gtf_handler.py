# -*- coding:utf-8 -*-
"""
@author: hbs
@date: 2018-10-18
Description:
    GTF format file annotates the element on genome. The entire content can be built as an Interval Tree.
    Chromosomes are the out layer of this tree, one chromosome can be separate into two strand(positive and negative).
    Each of one strand may contains a great number of genes. Genes on the strand is a tree construction, the transcripts
    on a certain gene can be also seen as an interval tree. Elements which form a particular transcript can be gethered
    and build an interval tree.
"""
from tree_node import GeneNode, TranscriptNode, ElementNode
from interval_tree import IntervalTree
import re
import os


class GtfReader:
    """
    extract useful informations from GTF files and build interval tree for each gene.
    """
    def __init__(self, gtf_file, element_priority):
        """
        :param gtf_file: the path of GTF file, type string.
        :param element_priority: the element which need to be extracted from the file with its priority. The smaller
                                 value, the higher priority, type dict.
        """
        self.gtf_file = gtf_file
        self.element_priority = element_priority
        self.target_element = self.element_priority.keys()
        self.gene_pattern = re.compile(r"gene_id \"([A-Z]+[0-9]+)\"")
        self.trans_pattern = re.compile(r"transcript_id \"([A-Z]+[0-9]+)\"")
        self.gtf_tree = {}

    def load_gtf(self):
        # get total line numer of the gtf file
        total_line = os.popen("wc -l %s" % self.gtf_file)
        total_line = int(re.sub(self.gtf_file, "", total_line.read()))
        with open(self.gtf_file, "r") as f:
            pre_chr, pre_gene, pre_trans = None, None, None
            trans_node_list, trans_interval_list = [], []
            element_interval_list, element_node_list = [], []
            positive_strand_gene_node_list, negative_strand_gene_node_list = [], []
            positive_strand_gene_interval_list, negative_strand_gene_interval_list = [], []
            pre_strand = None
            cur_line = 0
            for line in f:
                cur_line += 1
                if line.startswith("#"):
                    continue
                info = line.split("\t")
                # obtain the element name
                element = info[2]
                if element not in self.target_element:
                    continue

                chr_num, strand = info[0], info[6]
                if chr_num not in self.gtf_tree.keys():
                    self.gtf_tree[chr_num] = {}

                cur_trans = re.findall(self.trans_pattern, info[8])[0]
                if (cur_trans != pre_trans and pre_trans is not None) or cur_line == total_line:
                    # when transcript change, build the element interval tree and append it into trans_list,
                    # element_list will be clear simutaneously
                    element_tree = GtfReader.build_tree(element_node_list)
                    interval = (min(element_interval_list)[0], max(i[1] for i in element_interval_list))
                    transcript_node = TranscriptNode(interval, pre_trans, elements=element_tree)
                    trans_node_list.append(transcript_node)
                    trans_interval_list.append(interval)
                    element_interval_list.clear()
                    element_node_list.clear()

                element_start, element_end = int(info[3]), int(info[4])
                element_node = ElementNode((element_start, element_end), element)
                element_interval_list.append((element_start, element_end))
                element_node_list.append(element_node)

                cur_gene = re.findall(self.gene_pattern, info[8])[0]
                if (cur_gene != pre_gene and pre_gene is not None) or cur_line == total_line:
                    # when genge change, build the transcript interval tree and append it into gene_list,
                    # transcript_list will be clear simutaneously
                    transcript_tree = GtfReader.build_tree(trans_node_list)
                    interval = (min(trans_interval_list)[0], max(i[1] for i in trans_interval_list))
                    gene_node = GeneNode(interval, pre_gene, transcripts=transcript_tree)
                    if pre_strand == "+":
                        positive_strand_gene_node_list.append(gene_node)
                        positive_strand_gene_interval_list.append(interval)
                    else:
                        negative_strand_gene_node_list.append(gene_node)
                        negative_strand_gene_interval_list.append(interval)
                    trans_node_list.clear()
                    trans_interval_list.clear()

                if (chr_num != pre_chr and pre_chr is not None) or cur_line == total_line:
                    pos_strand_tree = GtfReader.build_tree(positive_strand_gene_node_list)
                    neg_strand_tree = GtfReader.build_tree(negative_strand_gene_node_list)
                    pos_strand_interval = (min(positive_strand_gene_interval_list)[0], max(i[1] for i in positive_strand_gene_interval_list))
                    neg_strand_interval = (min(negative_strand_gene_interval_list)[0], max(i[1] for i in negative_strand_gene_interval_list))
                    positive_strand_gene_node_list.clear()
                    positive_strand_gene_interval_list.clear()
                    negative_strand_gene_node_list.clear()
                    negative_strand_gene_interval_list.clear()
                    self.gtf_tree[pre_chr]["+"], self.gtf_tree[pre_chr]["-"] = {}, {}
                    self.gtf_tree[pre_chr]["+"]["interval"], self.gtf_tree[pre_chr]["+"]["gene_tree"] = pos_strand_interval, pos_strand_tree
                    self.gtf_tree[pre_chr]["-"]["interval"], self.gtf_tree[pre_chr]["-"]["gene_tree"] = neg_strand_interval, neg_strand_tree

                pre_trans = cur_trans
                pre_gene = cur_gene
                pre_chr = chr_num
                pre_strand = strand

    @staticmethod
    def build_tree(compose_list):
        """
        use the nodes in node list to build an interval tree
        :param compose_list: node list
        :return:
        """
        it = IntervalTree()
        for node in compose_list:
            it = it.insert_interval(it, node)

        return it


if __name__ == "__main__":
    # just testing code
    gr = GtfReader("/data/nanopore/merip_seq_data/metpeak_calling_res/peak_location/reference_files/example.gtf",
                   element_priority={"stop_codon": 1, "three_prime_utr": 2, "CDS": 3, "five_prime_utr": 4})
    gr.load_gtf()
