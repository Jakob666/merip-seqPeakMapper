# -*- coding:utf-8 -*-
"""
@author: hbs
@date: 2018-10-18
description:
    the node for building interval tree of GTF format file, class "Node" was the base class for gene, transcript and
    element. The relationship between the three child class is demonstrated as follow:
    1) one gene may has several transcript.
    2) a transcript consists of a group of element
    3) element on transcript is the smallest part which we take it into account
"""


class Node:
    """
    the node of gene on interval tree.
    """
    def __init__(self, interval, name, compose, color=None):
        assert interval[0] <= interval[1]
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.interval_start = int(interval[0])
        self.interval_end = int(interval[1])
        self.center = (self.interval_start + self.interval_end) // 2
        self.name = name
        self.compose = compose
        self.color = color


class GeneNode(Node):
    """
    the node of gene on interval tree.
    """
    def __init__(self, interval, gene_id, transcripts, color=None):
        """
        :param interval: interval of this node, type tuple
        :param gene_id: gene id
        :param transcripts: the transcips of a certain gene, type interval tree object
        :param color: the node color of a red-black tree
        """
        super(GeneNode, self).__init__(interval, gene_id, transcripts, color)


class TranscriptNode(Node):
    """
    the node of transcript on interval tree
    """
    def __init__(self, interval, transcript_id, elements, color=None):
        """
        :param interval: interval: interval of this node, type tuple
        :param transcript_id: transcript id
        :param elements: the elements of a certain transcriptome, type interval tree object
        :param color: the node color of a red-black tree
        """
        super(TranscriptNode, self).__init__(interval, transcript_id, elements, color)


class ElementNode(Node):
    """
    the node of element on interval tree
    """
    def __init__(self, interval, element_name, compose=None, color=None):
        super(ElementNode, self).__init__(interval, element_name, compose, color)
