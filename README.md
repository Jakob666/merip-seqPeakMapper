# 目录说明
* chr_gtf
> 以不同染色体分组得到的gtf数据，其中记录的内容为 chr、element、start、end和strand，即染色体号、元件名称、元件起始、元件终止和正负链记录。
> 相同转录本上的同一种元件的不同记录可能存在区域上的overlap。

* chr_peaks
> 以不同染色体分组得到的metpeak数据，其内容为 chr、strand、start、end和center，即染色体号、正负链记录、峰起始位点、峰终止位点、峰中心位点。
> 相邻的两条峰的记录的区间不存在overlap。

* reference_files
> 对peak进行位置锁定时所需要的参考文件，内部存在如下文件，
> simple.gtf: 使用 simplify_gtf.py 文件对原始的gtf文件进行了简化，仅保留RNA相关的gtf文件记录。
> peak.bed: 使用metpeak进行peak calling得到的文件。
> example.bed、example.gtf: 测试所用的文件。
> peak_loc.tsv: 记录定位到RNA元件中的peak的信息，包括染色体位置、正负链、peak起始位点、peak终止位点、peak中心位点、peak长度、元件名称、做分布图时的横坐标、元件起始位点、元件终止位点

# 脚本文件说明
* drop_duplicated_peak.py
> 将metpeak生成的不同的peak定位到转录本的元件中，这一过程使用simple.gtf进行注释。同一个peak可能覆盖了不同转录本的不同位置，
> 以优先级进行排序选取其中最优的一条记录作为最终结果，最优记录的选取依据的是元件，优先级从高到低 stop_codon > 3'utr > cds > 5'utr。
> 得到的结果最终会写入peak_loc.tsv文件中

* interval_tree.py
> 用于创建区间树对象，依据不同的转录本的不同的元件进行区间树的构建。
> 同时定义区间树查找算法，可传入peak的中心点确定peak是否落在该元件中。

* draw_fig.py
> 可用于对peak的分布进行可视化。
