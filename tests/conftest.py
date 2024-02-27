import pytest
import ttkbootstrap as ttk

from exaide import model as m


@pytest.fixture()
def root():
    return ttk.Window()


@pytest.fixture()
def claim():
    return """1.一种具有栅偏压补偿的MOS晶体管电路，其特征在于，至少包括：
电阻器元件；
MOS半导体组件，包括第一MOS半导体元件和第二MOS半导体元件；
其中，所述电阻器元件与所述第一MOS半导体元件串联连接，所述第二MOS半导体元件通过栅极与所述电阻器元件和所述第一MOS半导体元件连接。
2.根据权利要求1所述的MOS晶体管电路，其特征在于：所述电阻器元件为上拉电阻或下拉电阻。
3.根据权利要求1或2所述的MOS晶体管电路，其特征在于：所述MOS半导体组件包括第一NMOS晶体管和第二NMOS晶体管，其中，第一NMOS晶体管的栅极和所述电阻器元件的一端连接电源电压，第一NMOS晶体管和第二NMOS晶体管的源极接地，第二NMOS晶体管的栅极连接第一NMOS晶体管的漏极和所述电阻器元件的另一端，第二NMOS晶体管的漏极连接电流输出端。
4.根据权利要求3所述的MOS晶体管电路，其特征在于：所述电阻器元件的一端通过一PMOS晶体管连接电源电压，其中，所述PMOS晶体管的栅极连接控制信号端，源极连接电源电压，漏极连接所述电阻器元件的一端。
5.根据权利要求1或2所述的MOS晶体管电路，其特征在于：所述MOS半导体组件包括第一PMOS晶体管和第二PMOS晶体管，其中，第一PMOS晶体管的栅极和所述电阻器元件的一端接地，第一PMOS晶体管和第二PMOS晶体管的源极连接电源电压，第二PMOS晶体管的栅极连接第一PMOS晶体管的漏极和所述电阻器元件的另一端，第二PMOS晶体管的漏极连接电流输出端。
6.根据权利要求5所述的MOS晶体管电路，其特征在于：所述电阻器元件的一端通过一NMOS晶体管接地，其中，所述NMOS晶体管的栅极连接控制信号端，源极接地，漏极连接所述电阻器元件的一端。
7.根据权利要求1至6任一项所述的MOS晶体管电路，其特征在于：所述电阻器元件为在不同PVT工艺角下受影响较小的电阻元件。
8.根据权利要求7所述的MOS晶体管电路，其特征在于：所述电阻器元件为多晶硅电阻。
"""


@pytest.fixture()
def desc():
    return """一种图1具有栅偏压补偿的MOS晶体图1管电路图1、4(a)和8(d)

技术领域
[0001]本发明涉及集成电路领域，特别是涉及一种具有栅偏压补偿的MOS晶体管电路。

背景技术
[0002]半导体工业的快速发展使得在过去三十年间电子器件和信息技术得以传播。在硅（主要的半导体材料）片（芯片）上制作的集成电路（IC）能有效地和廉价地执行许多电子功能（计算、信号处理、信息存储等），并且它们实际上还用于现在的每个电子器件。
[0003]晶体管是IC中使用的基本电子元件。现代微处理器在略大于1cm2的硅片上采用了超过五百万个晶体管。通过缩小元件模块的尺寸，IC的尺寸相应缩小了。单个IC所需的面积越小，则可以制作在单个硅晶片上IC的数量越大。假设与每个晶片增加的芯片数量相比处理单个晶片的成本仅略微增加，则IC成本会显著降低。
[0004]晶体管是用作电子开关的三端的半导体器件：两端间的电流是由电压或施加到第三终端的电流控制的。现在制造的绝大部分IC使用金属氧化物半导体场效应晶体管（MOSFET）作为基本元件模块。在MOSFET中，金属（也可以是掺杂质的多晶硅材料）栅极控制图1所示的源极和漏极之间的基片上的半导体沟道中的电流。金属门电极和半导体沟道通过一层非常薄的氧化物层相互电绝缘（因此，金属氧化物半导体有时也称为金属绝缘体半导体或MISFET）。
[0005]MOSFET可以根据沟道导电类型分为n沟道和p沟道，其中，n沟道MOSFET（NMOSFET）在将一个相对于源极的高电压加到栅电极上时导通（使电流响应于加在源极和漏极端子之间的电压自由地流动）；p沟道MOSFET（PMOSFET）在将一个相对于源极的低电压加到栅电极上时导通。NMOSFET的源极端子通常连接低电位（例如，接地，0V），而PMOSFET的源极端子通常连接高电位（例如，电源电压，VDD）。理想的MOSFET结构只有在加到相对于源极的栅电极的电压VGS大于阈值电压VT时，载流子才能从源极流向漏极，即当︳VGS－VT︳＞0时，︳IDS︳≥0。
[0006]在n沟道MOSFET（NMOSFET）中，源极区和漏极区是掺了很多杂质的n型（即源极区和漏极区包括高密度的具有负电荷的导带电子），而沟道区是掺杂质的p型（即沟道区不具有高密度的导带电子，而具有充足的带正关联电荷的价带空穴）。导带电子只有在沟道表面上形成电子的n型反型层时才通过将适当大小的相对于源极的正栅电压从源极流向漏极。当源极端子在低电压偏置时（特别是CMOS电路），通过加一个高栅电压VG导通NMOSFET。
[0007]相反，在p沟道MOSFET（PMOSFET）中，源极区和漏极区是掺了很多杂质的p型，而沟道区是掺杂质的n型。只有当通过施加相对于源极的适当大小的负栅电压在沟道表面上形成电子的p型反型层时价带空穴才从源极流向漏极。当源极端子在高电压偏置时（特别是CMOS电路），通过加一个低栅电压VG导通NMOSFET。
[0008]在MOSFET的制造过程中，由于制造步骤的不一致，而引起的工艺参数的波动、电源电压以及电路工作的环境温度（Process、Supply Voltage、Temperature，PVT）的变化都会造成MOS参数的波动。在栅极和源极间电压VGS、栅极和漏极间电压VDS和沟道长宽比W/L不变的情况下，MOS的电阻随着PVT角的变化而改变，例如，在最佳角的电阻值可能小于最差角的电阻值的一半。
[0009]现有技术中考虑在半导体基板上，采用多晶硅或扩散层形成电阻元件，并将这个电阻元件作为终端电阻使用，但是，该电阻元件的电阻值在受到制造工艺、周围温度、施加电压等影响时仍然具有变动增大的倾向，因此，难以得到期望电阻值的高精度的电阻元件。

发明内容
[0010]鉴于以上所述现有技术的缺点，本发明的目的在于提供一种具有栅偏压补偿的MOS晶体管电路，用于解决现有技术中PVT的变化造成电路性能受影响较大的问题。
[0011]为实现上述目的及其他相关目的，本发明提供一种具有栅偏压补偿的MOS晶体管电路，其特征在于，至少包括：
[0012]一电阻器元件；
[0013]MOS半导体组件，包括第一MOS半导体元件和第二MOS半导体元件；
[0014]其中，所述电阻器元件与所述第一MOS半导体元件串联连接，所述第二MOS半导体元件通过栅极与所述电阻器元件和所述第一MOS半导体元件连接。
[0015]优选地，所述电阻器元件为上拉电阻或下拉电阻。
[0016]优选地，所述MOS半导体组件包括第一NMOS晶体管和第二NMOS晶体管，其中，第一NMOS晶体管的栅极和所述电阻器元件的一端连接电源电压，第一NMOS晶体管和第二NMOS晶体管的源极接地，第二NMOS晶体管的栅极连接第一NMOS晶体管的漏极和所述电阻器元件的另一端，第二NMOS晶体管的漏极连接电流输出端。
[0017]优选地，所述电阻器元件的一端通过一PMOS晶体管连接电源电压，其中，所述PMOS晶体管的栅极连接控制信号端，源极连接电源电压，漏极连接所述电阻器元件的一端。
[0018]优选地，所述MOS半导体组件包括第一PMOS晶体管和第二PMOS晶体管，其中，第一PMOS晶体管的栅极和所述电阻器元件的一端接地，第一PMOS晶体管和第二PMOS晶体管的源极连接电源电压，第二PMOS晶体管的栅极连接第一PMOS晶体管的漏极和所述电阻器元件的另一端，第二PMOS晶体管的漏极连接电流输出端。
[0019]优选地，所述电阻器元件的一端通过一NMOS晶体管接地，其中，所述NMOS晶体管的栅极连接控制信号端，源极接地，漏极连接所述电阻器元件的一端。
[0020]优选地，所述电阻器元件为在不同PVT工艺角下受影响较小的电阻元件。优选地，所述电阻器元件为多晶硅电阻。
[0021]如上所述，本发明的一种具有栅偏压补偿的MOS晶体管电路，具有以下有益效果：
[0022]首先，本发明根据在不同PVT工艺角下多晶硅电阻受影响较小，而MOS晶体管电阻受影响较大的特性，将多晶硅电阻与两个NMOS晶体管中的一个NMOS晶体管或两个PMOS晶体管中的一个PMOS晶体管串联，另一个NMOS晶体管或PMOS晶体管通过栅极与多晶硅电阻和NMOS晶体管或PMOS晶体管连接，在PVT变化时多晶硅电阻的变化率小于与其串联的NMOS晶体管或PMOS晶体管的等效电阻的变化率，从而使与其串联的NMOS晶体管或PMOS晶体管的偏置电压增大或减小，与该NMOS晶体管或PMOS晶体管连接的另一NMOS晶体管或PMOS晶体管的电压也相应增大或减小，继而补偿另一NMOS晶体管或PMOS晶体管迁移率的降低或升高，使得输出电流基本不受PVT变化的影响，避免了电路合格率的降低。
[0023]其次，在多晶硅电阻的另一端增加了具有开关功能的MOS晶体管，使得本发明的MOS晶体管电路在具有稳定电路性能的功能的同时，也降低了集成电路的功率损耗，从而可以将本发明的MOS晶体管电路更广泛地作为固定电阻元件在更多领域中使用。

附图说明
[0024]图1显示为现有技术中半导体场效应晶体管的结构示意图。
[0025]图2显示为本发明的具有栅偏压补偿的MOS晶体管电路的实施例1示意图。
[0026]图3显示为本发明的具有栅偏压补偿的MOS晶体管电路的实施例2示意图。
[0027]图4显示为本发明的具有栅偏压补偿的MOS晶体管电路的实施例3示意图。
[0028]图5显示为本发明的具有栅偏压补偿的MOS晶体管电路的实施例4示意图。

实施例
[0029]以下通过特定的具体实例说明本发明的实施方式，本领域技术人员可由本说明书所揭露的内容轻易地了解本发明的其他优点与功效。本发明还可以通过另外不同的具体实施方式加以实施或应用，本说明书中的各项细节也可以基于不同观点与应用，在没有背离本发明的精神下进行各种修饰或改变。
[0030]本发明的主要构思为：考虑到多晶硅电阻较少受PVT影响，但是电阻率较低，导致实现精确的大电阻时占用空间较大，而MOS晶体管尺寸较小，且能够轻易地达到高等效电阻，但是在不同PVT工艺角下电阻受影响较大。若能在融合多晶硅电阻和MOS晶体管的优势的同时消除各自的缺陷，则可将这两者广泛的应用于多个领域。基于该思路，本发明创造性地将多晶硅电阻和MOS晶体管组成偏压生成电路，组成的MOS晶体管电路在栅偏压作用下受PVT的变化影响极小，可作为固定电阻元件加以广泛地应用。
[0031]本发明的MOS晶体管电路包括：一电阻器元件；MOS半导体组件，包括第一MOS半导体元件和第二MOS半导体元件；其中，所述电阻器元件与所述第一MOS半导体元件串联连接，所述第二MOS半导体元件通过栅极与所述电阻器元件和所述第一MOS半导体元件连接。
[0032]需要说明的是，所述MOS半导体组件可以包括两个相同导电类型的MOS半导体元件，如两个NMOS晶体管或两个PMOS晶体管。所述电阻器元件与其中的一个晶体管串联连接。当所述MOS半导体组件包括两个NMOS晶体管时，所述电阻器元件作为上拉电阻，优选地，在所述电阻器元件和电源电压之间增加一个具有开关功能的PMOS晶体管。当所述MOS半导体组件包括两个PMOS晶体管时，所述电阻器元件作为下拉电阻，优选地，在所述电阻器元件和接地端之间增加一个具有开关功能的NMOS晶体管。需要说明的是，优选地，所述电阻器元件为在不同PVT工艺角下受影响较小的电阻元件。优选地，所述电阻器元件为多晶硅电阻。
[0033]需要说明的是，在MOSFET的实际制造过程中，在不同的晶片之间以及在不同的批次之间，MOSFET参数变化很大。为了在一定程度上减轻电路设计任务的困难，需要保证器件的性能在某个范围内，通常以报废超出这个性能范围的芯片的措施来严格控制预期的参数变化。这个性能范围通常以“工艺角”（Process Corner）的形式给出，其思想是：把NMOS晶体管和PMOS晶体管的速度波动范围限制在由四个角所确定的矩形内。这四个角分别是：快NFET和快PFET，慢NFET和慢PFET，快NFET和慢PFET，慢NFET和快PFET。例如，具有较薄的栅氧、较低阈值电压的晶体管，就落在快角附近。
[0034]如果采用5-corner模式会有TT、FF、SS、FS和SF5个corner。如TT指NFET典型工艺角&PFET典型工艺角（NFET-Typical corner&PFET-Typical corner）。其中,典型（Typical）指晶体管驱动电流是一个平均值，快（FAST）指驱动电流是其最大值，而慢（SLOW）指驱动电流是其最小值（此电流为Ids电流），也可以理解为载流子迁移率(Carrier mobility)的快慢。载流子迁移率是指载流子在单位电场作用下的平均漂移速度。
[0035]设计时除了要满足上述5个工艺角外，还需要满足电压与温度等条件，形成的组合称为PVT(process,voltage,temperature)条件。通常需要考虑找到最好最坏情况，时序分析(StaticTiming Analysis，STA)中将最好的条件(Best Case)定义为速度最快的情况，而最坏的条件(Worst Case)则相反。根据不同的仿真需要，会有不同的PVT组合。以下是几种标准的STA分析条件：最差PVT角(Worst Corner)：慢速（slow process），高温（high temperature），低压（low voltage）；典型PVT角(Typical Corner)：典型速度（typical process），典型温度（nominaltemperature），典型电压（nominal voltage）；最佳PVT角(Best Case Fast)：快速（fast process），低温（lowest temperature），高压（high voltage）。在最差PVT角条件下，载流子迁移率最小，在最佳PVT角条件下，载流子迁移率最大。
[0036]以下通过4个实施例说明本发明的构思，需要说明的是，下述实施例中所提供的图示仅以示意方式说明本发明的基本构想，遂图式中仅显示与本发明中有关的组件而非按照实际实施时的组件数目、形状及尺寸绘制，其实际实施时各组件的型态、数量及比例可为一种随意的改变，且其组件布局型态也可能更为复杂。
[0037]实施例1
[0038]请参阅图2本发明的具有栅偏压补偿的MOS晶体管电路的实施例1示意图。
[0039]该MOS晶体管电路包括：电阻器元件、第一NMOS晶体管和第二NMOS晶体管，其中，所述电阻器元件与第一NMOS晶体管串联连接，第二NMOS晶体管通过栅极与所述电阻器元件和第一NMOS晶体管连接。具体地，第一NMOS晶体管的栅极和所述电阻器元件的一端连接电源电压，第一NMOS晶体管和第二NMOS晶体管的源极接地，第二NMOS晶体管的栅极连接第一NMOS晶体管的漏极和所述电阻器元件的另一端，第二NMOS晶体管的漏极连接电流输出端。
[0040]如图2所示，M0为第二NMOS晶体管，M1为第一NMOS晶体管，R1为多晶硅电阻，M1的栅极和R1的一端连接电源电压VDD，M0和M1的源极接地（VSS=0），M0的栅极连接M1的漏极和R1另一端，M0的漏极连接电流输出端NET。
[0041]在该电路中，电源电压的电压VDD是恒定的，M1的过驱动电压大于源漏电压，使得M1工作在线性区，此时，M1相当于一个电阻，其等效电阻R2等于其饱和区跨导gm1的倒数，即：
[0042] R 2 = 1 g m 1 .
[0043]由于R1和R2串联，因此
[0044] V B = R 2 R 1 + R 2 V DD , M0的电流ID与VB成正比。
[0045]随着PVT工艺角的变化，R1和M1的等效电阻的变化率不同使得M0的栅偏压增大或减小，M0的过驱动电压也随之增大或减小，补偿了M0的载流子迁移率的降低或增加，从而使电流基本保持在典型角电流（典型角的工艺条件下的电流）左右。以下以工艺条件偏离典型PVT角条件最大的两个工艺角——最佳PVT角和最差PVT角为例说明：
[0046]相对于典型PVT角，在最差PVT角工艺条件下，在电源电压VDD不变的条件下，R1和M1的等效电阻R2均增大，但由于R1的电阻变化率小于R2的电阻变化率，因此R1增大的幅度小于R2增大的幅度。M1的分压变大，M0的栅极电压VB升高，由于M0的源极接地，因此，VB=VGS，如下式1所示，
[0047] I D = 1 2 μ n C ox W L ( V GS - V TH ) 2 - - - ( 1 )
[0048]其中，μn为载流子迁移率，Cox为栅极氧化层的电容，W和L分别为沟道的宽度和长度，VGS为栅极与源极之间的电压，VTH为阈值电压。在这里，忽略了沟道调制效应。当VB升高时，VGS升高，则M0的过驱动电压VGS—VTH亦升高，由于与典型PVT角相比，在最差PVT角工艺条件下，载流子迁移率μn降低，在Cox和W/L均不变的情况下，VGS—VTH的升高补偿了μn的下降，ID最差≈ID典型。
[0049]相对于典型PVT角，在最佳PVT角工艺条件下，在电源电压VDD不变的条件下，R1和M1的等效电阻R2均减小，但由于R1的电阻变化率小于R2的电阻变化率，因此R1减小的幅度小于R2减小的幅度。M1的分压变小，M0的栅极电压VB下降，也随之VGS下降，则M0的过驱动电压VGS—VTH亦下降。由于与典型PVT角相比，在最佳PVT角工艺条件下，载流子迁移率μn升高，在Cox和W/L均不变的情况下，VGS—VTH的下降补偿了μn的升高，ID最佳≈ID典型。
[0050]由此可以看出，ID最差≈ID典型≈ID最佳，同样可以推导出其他PVT角条件下MOS晶体管的输出电流与典型PVT角下的电流也几乎相同。
[0051]实施例2
[0052]请参阅图3本发明的具有栅偏压补偿的MOS晶体管电路的实施例2示意图。
[0053]与实施例1不同的是，本实施例增加了一个具有开关功能的PMOS晶体管。该MOS晶体管电路包括：电阻器元件、第一NMOS晶体管、第二NMOS晶体管和PMOS晶体管，其中，所述电阻器元件、PMOS晶体管与第一NMOS晶体管串联连接，第二NMOS晶体管通过栅极与所述电阻器元件和第一NMOS晶体管连接。具体地，第一NMOS晶体管的栅极和PMOS晶体管的源极连接电源电压，第一NMOS晶体管和第二NMOS晶体管的源极接地，第二NMOS晶体管的栅极连接第一NMOS晶体管的漏极和所述电阻器元件的一端，第二NMOS晶体管的漏极连接电流输出端，PMOS晶体管的栅极连接控制信号端，漏极连接所述电阻器元件的另一端。如图3所示，M0为第二NMOS晶体管，M1为第一NMOS晶体管，M3为PMOS晶体管，R1为多晶硅电阻，M1的栅极和M3的源极连接电源电压VDD，M0和M1的源极接地（VSS=0），M0的栅极连接M1的漏极和R1的一端，M0的漏极连接电流输出端NET，M3的栅极连接控制信号端REN，漏极连接R1的另一端。
[0054]当控制信号端REN为低时，PMOS晶体管M3打开（导通），当控制信号端REN为高时，PMOS晶体管M3关闭（截止），NMOS M1开启，M0的栅偏置点VB被拉到地，M0也截止，整个电路没有电流通过，由此减小了电路的功率消耗。
[0055]实施例3
[0056]请参阅图4本发明的具有栅偏压补偿的MOS晶体管电路的实施例3示意图。
[0057]该MOS晶体管电路包括：电阻器元件、第一PMOS晶体管和第二PMOS晶体管，其中，所述电阻器元件与第一PMOS晶体管串联连接，第二PMOS晶体管通过栅极与所述电阻器元件和第一PMOS晶体管连接。具体地，第一PMOS晶体管的栅极和所述电阻器元件的一端接地，第一PMOS晶体管和第二PMOS晶体管的源极连接电源电压，第二PMOS晶体管的栅极连接第一PMOS晶体管的漏极和所述电阻器元件的另一端，第二PMOS晶体管的漏极连接电流输出端。
[0058]如图4所示，M4为第一PMOS晶体管，M5为第二PMOS晶体管，R1为多晶硅电阻，M4的栅极和R1的一端接地（VSS=0），M4和M5的源极连接电源电压VDD，M5的栅极连接M4的漏极和R1另一端，M5的漏极连接电流输出端NET。
[0059]在该电路中，电源电压的电压VDD是恒定的，M4的过驱动电压大于源漏电压，使得M4工作在线性区，此时，M4相当于一个电阻，其等效电阻R3等于其饱和区跨导gm3的倒数，即：
[0060] R 3 = 1 g m 3 .
[0061]由于R1和R3串联，因此
[0062] V B = R 3 R 1 + R 3 VDD , M5的电流ID与VB成正比。
[0063]随着PVT工艺角的变化，R1和M4的等效电阻R3的变化率不同使得M5的栅偏压增大或减小，M5的过驱动电压也随之增大或减小，补偿了M5的载流子迁移率的降低或增加，从而使电流基本保持在典型角电流（典型角的工艺条件下的电流）左右。以下以工艺条件偏离典型PVT角条件最大的两个工艺角——最佳PVT角和最差PVT角为例说明：
[0064]相对于典型PVT角，在最差PVT角工艺条件下，在电源电压VDD不变的条件下，R1和M4的等效电阻R3均增大，但由于R1的电阻变化率小于R3的电阻变化率，因此R1增大的幅度小于R3增大的幅度。M4的分压变大，M5的栅极电压VB降低，M5的源极接电压VDD，因此，VB与VDD之间的电压即VGS升高，则M5的过驱动电压VGS—VTH亦升高，由于与典型PVT角相比，在最差PVT角工艺条件下，载流子迁移率μn降低，在Cox和W/L均不变的情况下，VGS—VTH的升高补偿了μn的下降，ID最差≈ID典型。
[0065]相对于典型PVT角，在最佳PVT角工艺条件下，在电源电压VDD不变的条件下，R1和M4的等效电阻R3均减小，但由于R1的电阻变化率小于R3的电阻变化率，因此R1减小的幅度小于R3减小的幅度。M4的分压变小，M5的栅极电压VB升高，VGS也随之下降，则M5的过驱动电压VGS—VTH亦下降。由于与典型PVT角相比，在最佳PVT角工艺条件下，载流子迁移率μn升高，在Cox和W/L均不变的情况下，VGS—VTH的下降补偿了μn的升高，ID最佳≈ID典型。
[0066]由此可以看出，ID最差≈ID典型≈ID最佳，同样可以推导出其他PVT角条件下MOS晶体管的输出电流与典型PVT角下的电流也几乎相同。
[0067]实施例4
[0068]请参阅图5本发明的具有栅偏压补偿的MOS晶体管电路的实施例4示意图。
[0069]与实施例3不同的是，本实施例增加了一个具有开关功能的NMOS晶体管。该MOS晶体管电路包括：电阻器元件、第一PMOS晶体管、第二PMOS晶体管和NMOS晶体管，其中，所述电阻器元件、第一PMOS晶体管和NMOS晶体管串联连接，第二PMOS晶体管通过栅极与所述电阻器元件和第一PMOS晶体管连接。具体地，第一PMOS晶体管的栅极和NMOS晶体管的源极接地，第一PMOS晶体管和第二PMOS晶体管的源极连接电源电压，第二PMOS晶体管的栅极连接第一PMOS晶体管的漏极和所述电阻器元件的一端，第二PMOS晶体管的漏极连接电流输出端，NMOS晶体管的栅极连接控制信号端，漏极连接所述电阻器元件的另一端。
[0070]如图5所示，M4为第一PMOS晶体管，M5为第二PMOS晶体管，R1为多晶硅电阻，M6为NMOS晶体管，M4的栅极和M6的源极接地（VSS=0），M4和M5的源极连接电源电压VDD，M5的栅极连接M4的漏极和R1的一端，M5的漏极连接电流输出端NET，M6的漏极连接R1的另一端，栅极连接控制信号端REN。
[0071]当控制信号端REN为高时，NMOS晶体管M6打开（导通），当控制信号端REN为低时，NMOS晶体管M6关闭（截止），PMOS M4开启，M5的栅偏置点VB被拉到地，M5也截止，整个电路没有电流通过，由此减小了电路的功率消耗。
[0072]综上所述，本发明的一种具有栅偏压补偿的MOS晶体管电路，具有以下有益效果：
[0073]首先，本发明根据在不同PVT工艺角下多晶硅电阻受影响较小，而MOS晶体管电阻受影响较大的特性，将多晶硅电阻与两个NMOS晶体管中的一个NMOS晶体管或两个PMOS晶体管中的一个PMOS晶体管串联，另一个NMOS晶体管或PMOS晶体管通过栅极与多晶硅电阻和NMOS晶体管或PMOS晶体管连接，在PVT变化时多晶硅电阻的变化率小于与其串联的NMOS晶体管或PMOS晶体管的等效电阻的变化率，从而使与其串联的NMOS晶体管或PMOS晶体管的偏置电压增大或减小，与该NMOS晶体管或PMOS晶体管连接的另一NMOS晶体管或PMOS晶体管的电压也相应增大或减小，继而补偿另一NMOS晶体管或PMOS晶体管迁移率的降低或升高，（还有一种情况是电阻CMOS器件的偏执在最佳工艺角时降低，补偿其沟道迁移率的增加）使得输出电流基本不受PVT变化的影响，避免了电路合格率的降低。
[0074]其次，在多晶硅电阻的另一端增加了具有开关功能的MOS晶体管，使得本发明的MOS晶体管电路在具有稳定电路性能的功能的同时，也降低了集成电路的功率损耗，从而可以将本发明的MOS晶体管电路更广泛地作为固定电阻元件在更多领域中使用。
[0075]所以，本发明有效克服了现有技术中的种种缺点而具高度产业利用价值。
[0076]上述实施例仅例示性说明本发明的原理及其功效，而非用于限制本发明。任何熟悉此技术的人士皆可在不违背本发明的精神及范畴下，对上述实施例进行修饰或改变。因此，举凡所属技术领域中具有通常知识者在未脱离本发明所揭示的精神与技术思想下所完成的一切等效修饰或改变，仍应由本发明的权利要求所涵盖。
"""
