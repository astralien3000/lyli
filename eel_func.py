
class Func(object):
    class Return(object):
        def __init__(self, val):
            self.val = val
    def __init__(self, params, exp, ctx):
        self.params = params
        self.exp = exp
        self.ctx = ctx
    def __call__(self, *args):
        from eel_eval import *
        from eel_context import *
        import eel_cur_ctx
        prev_ctx = eel_cur_ctx.cur_ctx
        eel_cur_ctx.cur_ctx =  Context(zip(self.params, args), self.ctx)
        ret = None
        for e in self.exp:
            tmp = eval(e)
            if isinstance(tmp, Func.Return):
                ret = tmp.val
                break
        eel_cur_ctx.cur_ctx = prev_ctx
        return ret
