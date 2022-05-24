import inspect
import ast


def get_caller_signature(function: callable, depth: int = 1):
    stack_frame = inspect.stack()
    inspected_frame = stack_frame[2 + depth]
    code = "".join(inspected_frame.code_context).strip()
    parsed_code = ast.parse(code)
    signature = inspect.signature(function)
    del stack_frame
    try:
        node = parsed_code.body[0]
        if isinstance(node, ast.Assign):
           node = node.value
        assert isinstance(node, ast.Call)
        args = []
        kwargs = {}

        for arg in node.args:
            args.append(arg.id)
        for kwarg in node.keywords:
            kwargs[kwarg.arg] = kwarg.value.id

    except Exception:
        return None
    return signature.bind(*args, **kwargs)

