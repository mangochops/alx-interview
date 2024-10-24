#!/usr/bin/python3
import sys
import re

def extract_input(input_line):
    '''Extracts sections of a line of an HTTP request log.'''
    # Updated log format pattern to match IP, date, request, status code, and file size
    log_fmt = (
        r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - \[.*?\] '
        r'"GET /projects/260 HTTP/1.1" (?P<status_code>\d{3}) (?P<file_size>\d+)'
    )
    
    resp_match = re.match(log_fmt, input_line)
    if resp_match is not None:
        return {
            'status_code': resp_match.group('status_code'),
            'file_size': int(resp_match.group('file_size'))
        }
    return None  # Return None for invalid lines

def print_statistics(total_file_size, status_codes_stats):
    '''Prints the accumulated statistics of the HTTP request log.'''
    print(f'File size: {total_file_size}')
    for status_code, count in sorted(status_codes_stats.items()):
        if count > 0:
            print(f'{status_code}: {count}')

def run():
    '''Starts the log parser.'''
    total_file_size = 0
    status_codes_stats = {code: 0 for code in ['200', '301', '400', '401', '403', '404', '405', '500']}
    line_count = 0

    try:
        for line in sys.stdin:
            log_data = extract_input(line.strip())
            if log_data:
                # Update file size
                total_file_size += log_data['file_size']
                # Update status code count
                status_code = log_data['status_code']
                if status_code in status_codes_stats:
                    status_codes_stats[status_code] += 1
            
            line_count += 1
            # Print statistics after every 10 lines
            if line_count % 10 == 0:
                print_statistics(total_file_size, status_codes_stats)
    
    except KeyboardInterrupt:
        # Print statistics on keyboard interruption (CTRL + C)
        print_statistics(total_file_size, status_codes_stats)
        raise

    # Final print in case of EOF (end of input)
    print_statistics(total_file_size, status_codes_stats)

if __name__ == '__main__':
    run()
