from projects.football_intelligence.src.ingestion.real_dataset_builder import RealDatasetBuilder,DatasetConfig

def test_builder(tmp_path):
    class C:
        def get(self,path,params):
            if path=="/fixtures":
                return {"response":[{"fixture":{"id":10,"timestamp":1,"status":{"short":"FT"}},"league":{"id":39,"name":"Test","season":2025},"teams":{"home":{"id":1},"away":{"id":2}},"goals":{"home":2,"away":1}}]}
            return {"response":[{"bookmakers":[]}]}
    p=tmp_path/"d.jsonl"
    n=RealDatasetBuilder(C()).build_skeleton(DatasetConfig(39,2025),p)
    assert n==1 and "event_id" in p.read_text()
