import config
from flask import Flask, request, jsonify
# import flask

import glosses_edit, expressions_edit, languages_retrieve, units_edit, get_lemmas, get_poses
import glosses_simple, existing_glossings, save_new_expression
import get_frames
import glossing_info
import save_new_frame
import operations_w_frames
import get_routines
import save_routine
import search_from_interface
import cxs
import modifying_data
from get_examples import get_examples

app = Flask(__name__)

@app.route('/glosses', methods=['GET', 'POST'])
def glosses():
    if request.method == 'GET':
        print('get query received')
        return glosses_edit.export_table()
    elif request.method == 'POST':
        print('new gloss info received', request.get_json())
        updated_row = request.get_json()
        return glosses_edit.update_gloss(updated_row)

@app.route('/glosses-simplified', methods=['GET'])
def get_glosses_simplified():
    if request.method == 'GET':
        return glosses_simple.export_table()

@app.route('/glosses-remove', methods=['GET', 'POST'])
def glosses_remove():
    if request.method == 'POST':
        print('request to mark useless received', request.get_json())
        useless_gloss_id = request.get_json()['useless_gloss_id']
        return glosses_edit.remove_gloss(useless_gloss_id)

@app.route('/expressions', methods=['GET', 'POST'])
def expressions():
    if request.method == 'POST':
        print('post query received')
        requested_lang_id = request.get_json()["lang_id"]
        print(requested_lang_id)
        return expressions_edit.export_table(requested_lang_id)

@app.route('/languages', methods=['GET', 'POST'])
def languages():
    if request.method == 'GET':
        print('get query received')
        return languages_retrieve.export_table()

@app.route('/units-suggestions', methods=['GET', 'POST'])
def units_suggestions():
    if request.method == 'POST':
        received = request.get_json()
        lang_id = received["lang_id"]
        units = received["units"]
        print('units-suggestions', lang_id, units)
        return units_edit.export_mult_units_info(lang_id, units)

@app.route('/lemmas', methods=['GET', 'POST'])
def provide_lemmas():
    if request.method == 'POST':
        received = request.get_json()
        lang_id = received["lang_id"]
        return get_lemmas.language_lemmas(lang_id)

@app.route('/poses', methods=['GET', 'POST'])
def provide_poses():
    if request.method == 'POST':
        received = request.get_json()
        lang_id = received["lang_id"]
        return get_poses.language_poses(lang_id)

@app.route('/morphs-vs-glosses', methods=['GET', 'POST'])
def provide_morphs():
    if request.method == 'POST':
        received = request.get_json()
        # print('morphs-vs-glosses', received)
        # lang_id = received["lang_id"]
        # units_data = received["units"]
        # print(units_data)
        return existing_glossings.multiple_units(received)

@app.route('/glossing-examples', methods=['POST'])
def provide_glossing_examples():
    if request.method == 'POST':
        received = request.get_json()
        gl_id = received['gloss_id']
        return glossing_info.glossing_examples(gl_id) | glossing_info.get_lang_stats(gl_id)

@app.route('/submit-expression', methods=['POST'])
def fetch_expression():
    if request.method == 'POST':
        received = request.get_json()[0]
        print(received)
        inserted_id = save_new_expression.insert_expression(received)
        return {'inserted_id': inserted_id}
    
@app.route('/submit-frame', methods=['POST'])
def fetch_frame():
    if request.method == 'POST':
        received = request.get_json()
        result = save_new_frame.insert_frame(received)
        return result

@app.route('/get-structure-tags', methods=['POST'])
def update_structure_data():
    if request.method == 'POST':
        struct = request.get_json()['struct']
        return operations_w_frames.get_tags_on_structure(struct)

@app.route('/get-frame-tags', methods=['GET'])
def get_frame_tags():
    if request.method == 'GET':
        return operations_w_frames.get_general_frame_tags()
    
@app.route('/get-all-frames', methods=['POST'])
def get_all_frames():
    if request.method == 'POST':
        lang_id = request.get_json()['lang_id']
        table = get_frames.frames_from_db(lang_id)
        if table is not None:
            return table
        else:
            return []
        
@app.route('/get-routines-for-frame', methods=['POST'])
def get_routines_for_frame():
    if request.method == 'POST':
        frame_id = request.get_json()['frame_id']
        return operations_w_frames.get_linked_routines(frame_id)

@app.route('/get-all-routines', methods=['POST'])
def get_all_routines():
    if request.method == 'POST':
        lang_id = request.get_json()['lang_id']
        table = get_routines.routines_from_db(lang_id)
        if table is not None:
            return table
        else:
            return []

@app.route('/get-routines-simple', methods=['POST', 'GET'])
def get_routines_simple():
    if request.method == 'POST':
        lang_id = request.get_json()['lang_id']
        table = get_routines.routines_bare(lang_id)
        if table is not None:
            return table
        else:
            return []
    if request.method == 'GET':
        return get_routines.routines_bare(lang_id=None)


@app.route('/get-full-expressions', methods=['POST'])
def get_expressions_full():
    if request.method == 'POST':
        lang = request.get_json()['lang']
        return expressions_edit.get_annotated_exprs(lang)
    
@app.route('/get-specific-expressions', methods=['POST'])
def get_expressions_specific():
    if request.method == 'POST':
        ids = request.get_json()['ids']
        return expressions_edit.get_annotated_expr_by_id(ids)

@app.route('/save-new-routine', methods=['POST'])
def save_new_routine():
    if request.method == 'POST':
        data = request.get_json()
        return save_routine.save_routine(data)

@app.route('/save-frame-edits', methods=['POST'])
def save_frame_edits():
    if request.method == 'POST':
        data = request.get_json()
        return operations_w_frames.save_edits(data)
    
@app.route('/delete-frame', methods=['POST'])
def delete_frame():
    if request.method == 'POST':
        frame_id = request.get_json()['frame_id']
        return operations_w_frames.delete_frame(frame_id)

@app.route('/example-sources', methods=['GET'])
def get_sources():
    if request.method == 'GET':
        return search_from_interface.ex_sources()
    
@app.route('/get-constructions', methods=['GET'])
def get_cxs():
    if request.method == 'GET':
        return cxs.all_cxs()

@app.route('/get-constructions-simple', methods=['GET'])
def get_cxs_simple():
    if request.method == 'GET':
        return cxs.cx_table()

@app.route('/get-one-construction', methods=['POST'])
def get_cx_info():
    if request.method == 'POST':
        cx_id = request.get_json()['cx_id']
        return cxs.cx_info(cx_id)
    
@app.route('/update-construction-info', methods=['POST'])
def update_cx():
    if request.method == 'POST':
        cx_info = request.get_json()
        return cxs.update_cx(cx_info)

@app.route('/add-construction', methods=['POST'])
def add_cx():
    if request.method=='POST':
        data = request.get_json()
        return cxs.add_cx(data)

@app.route('/reductions', methods=['GET'])
def get_reds():
    if request.method=='GET':
        return cxs.get_reductions()

@app.route('/delete-routine', methods=['POST'])
def delete_routine():
    if request.method == 'POST':
        routine_id = request.get_json()
        return modifying_data.delete_routine(routine_id)

@app.route('/generate-examples', methods=['POST'])
def generate_examples():
    if request.method == 'POST':
        data = request.get_json()
        return get_examples(data['exprs'], data['lang_id'], data['page_num'])

@app.route('/get-routine', methods=['POST'])
def get_one_routine():
    if request.method == 'POST':
        routine_id = request.get_json()['routine_id']
        return get_routines.get_routine(routine_id)

@app.route('/change-expression-refs', methods=['POST'])
def change_expression_refs():
    if request.method == 'POST':
        data = request.get_json()
        routine_id = data['routine_id']
        comprehensive_expr_ids_list = data['expr_ids']
        return expressions_edit.rereference_exprs(routine_id, comprehensive_expr_ids_list)

@app.route('/change-cx-refs', methods=['POST'])
def change_cx_refs():
    if request.method == 'POST':
        data = request.get_json()
        routine_id = data['routine_id']
        comprehensive_cx_ids_list = data['cx_ids']
        return cxs.rereference_cxs(routine_id, comprehensive_cx_ids_list)

@app.route('/change-frame-refs', methods=['POST'])
def change_frame_refs():
    if request.method == 'POST':
        data = request.get_json()
        routine_id = data['routine_id']
        comprehensive_frame_ids_list = data['frame_ids']
        return get_frames.rereference_frames(routine_id, comprehensive_frame_ids_list)

@app.route('/change-cx-info', methods=['POST'])
def change_cx_info():
    if request.method == 'POST':
        data = request.get_json()
        routine_id = data['routine_id']
        comprehensive_reduction_list = data['cx_reductions']
        comprehensive_cx_example_list = data['cx_examples']
        return cxs.change_info(routine_id, comprehensive_cx_example_list, comprehensive_reduction_list)
    
@app.route('/change-frame-info', methods=['POST'])
def change_frame_info():
    if request.method == 'POST':
        frame = request.get_json()
        return modifying_data.change_frame_info(frame)

@app.route('/change-routine', methods=['POST'])
def change_routine():
    if request.method == 'POST':
        data = request.get_json()
        routine_id = data['routine_id']
        new_routine_name = data['routine']
        return units_edit.change_routine(routine_id, new_routine_name)
    
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', config.UI_SERVER)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == '__main__':
    app.run("localhost", config.API_SERVER)

