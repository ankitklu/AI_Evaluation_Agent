from pydantic import BaseModel, Field

class Answer(BaseModel):
    answer: str = Field(description="the answer that is need for the user question")
    conversation:bool = Field(description="THis is an indicator to know if the conversation"\
                              "should still continue or no. of the agent has made the decision about the refun this should be false"\
                              "if thr conersation still need more talk then it's True", default= True)


class PurchaseItem(BaseModel):
    name : str = Field(description= "name of the item purchased")


