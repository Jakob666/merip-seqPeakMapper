# -*- coding:utf-8 -*-
"""
@author: hbs
@date: 2018-9-27
description:
    区间树算法
"""


class IntervalTree:
    def __init__(self):
        self.root = None

    def left_rotate(self, node):
        """
        红黑树的左旋，以node为支点向左旋转
        :param node:
        :return:
        """
        assert self.root is not None and node is not None
        # 旋转后变换到该位置的节点（即node的右子节点）
        y = node.right_child
        node.right_child = y.left_child
        if y.left_child is not None:
            y.left_child.parent = node

        # 如果node是根节点
        if node.parent is None:
            self.root = y
        # 如果node是其父的左子节点
        elif node == node.parent.left_child:
            node.parent.left_child = y
        # 如果node是其父的右子节点
        else:
            node.parent.right_child = y

        node.parent = y

        return None

    def right_rotate(self, node):
        """
        红黑树的右旋，以node为支点向右旋转
        :param node:
        :return:
        """
        assert self.root is not None and node is not None
        # 旋转后变换到该位置的节点（即node的左子节点）
        y = node.left_child
        node.left_child = y.right_child
        if y.right_child is not None:
            y.right_child.parent = node

        # 如果node是根节点
        if node.parent is None:
            self.root = y
        # 如果node是其父的左子节点
        elif node == node.parent.left_child:
            node.parent.left_child = y
        # 如果node是其父的右子节点
        else:
            node.parent.right_child = y

        node.parent = y

        return None

    def insert_interval(self, tree, node):
        """
        向区间树中插入新节点
        :param tree: 区间树对象
        :param node: 新的节点
        :return:
        """
        assert node is not None
        if tree.root is None:
            tree.root = node
            return tree
        # tag标记用于记录最终的父节点
        tag = None
        tree_root = tree.root
        while tree_root is not None:
            tag = tree_root
            if node.interval_end <= tree_root.interval_start:
                tree_root = tree_root.left_child
            elif node.interval_start >= tree_root.interval_end:
                tree_root = tree_root.right_child
            else:
                if node.center < tree_root.center:
                    tree_root = tree_root.left_child
                else:
                    tree_root = tree_root.right_child

        node.parent = tag

        if node.interval_end < tag.interval_start:
            tag.left_child = node
        elif node.interval_start >= tag.interval_end:
            tag.right_child = node
        else:
            if node.center < tag.center:
                tag.left_child = node
            else:
                tag.right_child = node

        node.color = 0
        # self.insert_fix(tree, node)

        return tree

    def insert_fix(self, tree, node):
        """
        插入节点后维持红黑树的性质不变
        :param tree: 区间树对象
        :param node: 新插入的节点
        :return:
        """
        while node.parent is not None and node.parent.color == 0:
            # 如果新插入节点的父节点是祖父节点的左子节点
            if node.parent.parent is not None and node.parent == node.parent.parent.left_child:
                # 记录其叔叔节点
                uncle = node.parent.parent.right_child
                if uncle is not None and uncle.color == 0:
                    node.parent.color = 1
                    node.parent.parent.color = 0
                    # 这一步很关键
                    node = node.parent.parent
                else:
                    if node == node.parent.left_child:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 1
                    node.parent.parent.color = 0
                    self.left_rotate(node)
        # 根节点必需是黑色
        tree.root.color = 1
        return tree

    def delete_interval(self, tree, node):
        """
        删除区间树中的节点
        :param tree: 区间树对象
        :param node: 要删除的节点对象
        :return:
        """
        assert node is not None and tree is not None
        # 这次还不需要
        pass

    def delete_and_fix(self, node):
        """
        删除节点后位置红黑树性质不变
        :param node:
        :return:
        """
        pass

    def search(self, tree_root, node_center):
        """
        红黑树中查找区间
        :param tree_root: 区间树对象的根节点
        :param node_center:
        :return:
        """
        search_res = []
        if tree_root is not None:
            tree_root_start = tree_root.interval_start
            tree_root_end = tree_root.interval_end

            if node_center in range(tree_root_start, tree_root_end+1):
                search_res.append(tree_root)

            if node_center < tree_root.center:
                search_res += self.search(tree_root.left_child, node_center)
            else:
                res = self.search(tree_root.right_child, node_center)
                search_res += res
        return search_res

    def is_overlap(self, interval1, interval2):
        """
        判断两个区间是否有重叠
        :param interval1:
        :param interval2:
        :return:
        """
        overlapped = False
        # 相交的情况1:       p1 --------------------.min([interval1[1],interval2[1]])
        # max([[interval1[0],interval2[0]]) .------------ p2
        if max([interval1[0], interval2[0]]) <= min([interval1[1], interval2[1]]):
            overlapped = True

        # 相交的情况2:   不满足 p1 -------         或               p1 --------的情况
        #                              p2 ------     --------- p2
        elif not (interval1[0] > interval2[1] or interval1[1] < interval2[0]):
            overlapped = True
        return overlapped


