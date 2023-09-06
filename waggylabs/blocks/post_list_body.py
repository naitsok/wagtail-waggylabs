from waggylabs.blocks.base_body import BaseBodyBlock
from waggylabs.blocks.post_list import PostListBlock

        
class PostListBodyBlock(BaseBodyBlock):
    """Post list body block has specific additional blocks."""
    post_list = PostListBlock()
    
    class Meta:
        block_counts = {
            'post_list': { 'max_num': 1 },
        }