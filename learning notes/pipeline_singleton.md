### singleton
为何在embeddings.py中写get_model()这个懒加载函数，而非直接在文件顶部model = SentenceTransformer(...)?
原因：加载这个模型本身有开销（读取几百MB的权重文件到内存），如果每次调用 compute_embedding 都重新加载一次，程序会慢到不能用。用一个全局变量做缓存，保证整个程序生命周期内只加载一次——这个模式叫单例（singleton），是个很通用的工程模式，写任何"初始化成本高、但要被重复调用"的资源（数据库连接、模型、API客户端）都会用到。

### database migration
ALTER TABLE ADD COLUMN 这几行是"数据库迁移"（schema migration）的雏形——你已经有 10 条真实数据在库里了，不能因为要加一个新字段就删库重建,所以要写"检测缺列 → 补列"的兼容逻辑。

### assert 断言
很实用的调试工具:主动构造检查点,若数据没对上会让程序崩溃报错。写断言去验证假设。