
import stages.pipe.http_pipe as http_pipe
import stages.pipe.random_pipe as random_pipe
import stages.pipe.sin_pipe as sin_pipe
import stages.pipe.cell4g as cell4g_pipe

def pipe(config):
    
    if config.get('pipe').get('type') == 'http':
        return http_pipe.pipe(config)

    if config.get('pipe').get('type') == 'random':
        return random_pipe.pipe(config)

    if config.get('pipe').get('type') == 'sin':
        return sin_pipe.pipe(config)
    
    if config.get('pipe').get('type') == 'cell4g':
        return cell4g_pipe.pipe(config)

    raise Exception(f'Invalid pipe type: {config.get("pipe").get("type")}')
